MAIN_TEMPLATE="""
options:
  machineType: 'E2_HIGHCPU_32'
steps:
- name: 'gcr.io/cloud-builders/docker'
  id: dockersecret
  entrypoint: 'bash'
  args: ['-c', 'docker login --username=$_USERNAME --password=$$PASSWORD']
  secretEnv: ['PASSWORD']
- name: 'gcr.io/cloud-builders/docker'
  id: 'initialize-qemu'
  args: ['run', '--privileged', '--rm', 'tonistiigi/binfmt', '--install', 'all']
  waitFor: ['dockersecret']
- name: 'gcr.io/cloud-builders/docker'
  id: 'create-and-select-builder'
  args: ['buildx', 'create', '--name', 'multi-arch-builder', '--use']
  waitFor: ['initialize-qemu']
{BUILDSTEPS}
images:
{GCR_IO_TAGS_SORTED}
secrets:
- kmsKeyName: projects/google.com:cloudsdktool/locations/global/keyRings/docker/cryptoKeys/dockerhub-password
  secretEnv:
    PASSWORD: |
        CiQA9btlfpg/kWmwXQvrNXtkVpu2tDdD2VOi1FYd3mmjCUGaK4YSNwC8sn1MepjracHAg8VAQEWm
        s26BTGccqD1NTS83DGFdY9moRGhSPm4WJKCg2tTQKYeTfdqUjjM=
timeout: 7200s
options:
  env:
  - 'DOCKER_CLI_EXPERIMENTAL=enabled'
substitutions:
  _DOCKER_BUILDX_PLATFORMS: 'linux/amd64,linux/arm/v7,linux/arm64'"""

GCRIO_PROJECT='google.com/cloudsdktool'
GCR_PREFIXES = ['gcr.io', 'eu.gcr.io', 'asia.gcr.io', 'us.gcr.io']
DOCKERHUB_PREFIX='google'
OLD_NAME='cloud-sdk'
REBRAND_NAME='google-cloud-cli'
IMAGES=['alpine', 'debian_slim', 'default', 'debian_component_based', 'emulators']
LABEL_FOR_IMAGE={
    'alpine': 'alpine',
    'debian_slim': 'slim',
    'default': '',
    'debian_component_based': 'debian_component_based',
    'emulators': 'emulators'
    }

# Make all the tags and save them
tags={}
for i in IMAGES:
    tags[i]=[]
    label_name = LABEL_FOR_IMAGE[i]
    label_without_tag = label_name
    label_with_tag = label_name
    maybe_hypen = '-'
    if i == 'default':
        label_without_tag = 'latest'
        maybe_hypen = ''

    # Make dockerhub tags for i
    tags[i].append('\'{dockerhub_prefix}/{old_name}:{label}\''
         .format(dockerhub_prefix=DOCKERHUB_PREFIX,
                 old_name=OLD_NAME,
                 label=label_without_tag))
    tags[i].append('\'{dockerhub_prefix}/{old_name}:$TAG_NAME{maybe_hypen}{label}\''
         .format(dockerhub_prefix=DOCKERHUB_PREFIX,
                 old_name=OLD_NAME,
                 maybe_hypen=maybe_hypen,
                 label=label_with_tag))
    # Make gcr tags for i
    for gcr_prefix in GCR_PREFIXES:
        tags[i].append(
            '\'{gcrprefix}/{gcrio_project}/{old_name}:{label}\''
            .format(gcrprefix=gcr_prefix,
                    gcrio_project=GCRIO_PROJECT,
                    old_name=OLD_NAME,
                    label=label_without_tag))
        tags[i].append(
            '\'{gcr_prefix}/{gcrio_project}/{old_name}:$TAG_NAME{maybe_hypen}{label}\''
            .format(gcr_prefix=gcr_prefix,
                    gcrio_project=GCRIO_PROJECT,
                    old_name=OLD_NAME,
                    maybe_hypen=maybe_hypen,
                    label=label_with_tag))
        tags[i].append(
            '\'{gcrprefix}/{gcrio_project}/{rebrand_name}:{label}\''
            .format(gcrprefix=gcr_prefix,
                    gcrio_project=GCRIO_PROJECT,
                    rebrand_name=REBRAND_NAME,
                    label=label_without_tag))
        tags[i].append(
            '\'{gcr_prefix}/{gcrio_project}/{rebrand_name}:$TAG_NAME{maybe_hypen}{label}\''
            .format(gcr_prefix=gcr_prefix,
                    gcrio_project=GCRIO_PROJECT,
                    rebrand_name=REBRAND_NAME,
                    maybe_hypen=maybe_hypen,
                    label=label_with_tag))
build_steps=''
for i in IMAGES:
    image_directory = '{}/'.format(i)
    if i == 'default':
        image_directory = '.'

    build_step = """- name: 'gcr.io/cloud-builders/docker'
  id: {image_name}
  args: ['buildx', 'build', '--platform', '$_DOCKER_BUILDX_PLATFORMS', {tags}, '--push', '{image_directory}']
  waitFor: ['create-and-select-builder']"""
    output_build_step = build_step.format(
        image_name=i,
        tags=', '.join(['\'-t\', {}'.format(t) for t in  tags[i]]),
        image_directory=image_directory)
    if len(build_steps) > 0:
        build_steps+='\n'
    build_steps+=output_build_step

all_gcr_io_tags_for_images=''
all_images_tags=[]
for i in IMAGES:
    all_images_tags.extend([t for t in tags[i] if not t.startswith('\'google/cloud-sdk')])
for tag in sorted(all_images_tags):
    if len(all_gcr_io_tags_for_images) > 0:
        all_gcr_io_tags_for_images+='\n'
    all_gcr_io_tags_for_images+='- {}'.format(tag)

print(MAIN_TEMPLATE.format(
    BUILDSTEPS=build_steps,
    GCR_IO_TAGS_SORTED=all_gcr_io_tags_for_images
    ))
