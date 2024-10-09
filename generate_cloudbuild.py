MAIN_TEMPLATE="""# PROD BUILDING STEPS
options:
  logging: GCS_ONLY
  machineType: 'E2_HIGHCPU_32'
  env:
    - DOCKER_CLI_EXPERIMENTAL=enabled
logsBucket: 'gs://cloud-sdk-docker-build-logs'
steps:
- name: 'tonistiigi/binfmt:qemu-v6.2.0'
  args:
  - '--install'
  - 'all'
- name: 'gcr.io/cloud-builders/docker'
  id: multi_arch_step1
  args:
  - 'buildx'
  - 'create'
  - '--name'
  - 'mybuilder'
- name: 'gcr.io/cloud-builders/docker'
  id: multi_arch_step2
  args:
  - 'buildx'
  - 'use'
  - 'mybuilder'
  waitFor: ['multi_arch_step1']
- name: 'gcr.io/cloud-builders/docker'
  id: multi_arch_step3
  args:
  - 'buildx'
  - 'inspect'
  - '--bootstrap'
  waitFor: ['multi_arch_step2']
{BUILDSTEPS}
# END OF PROD BUILDING STEPS
{MULTIARCH_BUILDSTEPS}
- name: 'gcr.io/cloud-builders/docker'
  id: dockersecret
  entrypoint: 'bash'
  args: ['-c', 'docker login --username=$_USERNAME --password=$$PASSWORD']
  secretEnv: ['PASSWORD']
{DOCKER_PUSHSTEPS}
images:
{GCR_IO_TAGS_SORTED}
secrets:
- kmsKeyName: projects/google.com:cloudsdktool/locations/global/keyRings/docker/cryptoKeys/dockerhub-password
  secretEnv:
    PASSWORD: |
        CiQA9btlfpg/kWmwXQvrNXtkVpu2tDdD2VOi1FYd3mmjCUGaK4YSNwC8sn1MepjracHAg8VAQEWm
        s26BTGccqD1NTS83DGFdY9moRGhSPm4WJKCg2tTQKYeTfdqUjjM=
timeout: 7200s"""

GCRIO_PROJECT='google.com/cloudsdktool'
GCR_PREFIXES = [('us-docker.pkg.dev', 'gcr.io'), ('us-docker.pkg.dev', 'us.gcr.io'), ('europe-docker.pkg.dev','eu.gcr.io'), ('asia-docker.pkg.dev', 'asia.gcr.io')]
DOCKERHUB_PREFIX='google'
OLD_NAME='cloud-sdk'
REBRAND_NAME='google-cloud-cli'
IMAGES=['alpine', 'debian_slim', 'default', 'debian_component_based', 'emulators', 'stable']
MULTI_ARCH=['debian_slim', 'debian_component_based', 'alpine', 'emulators', 'stable']
LABEL_FOR_IMAGE={
    'alpine': 'alpine',
    'debian_slim': 'slim',
    'default': '',
    'debian_component_based': 'debian_component_based',
    'emulators': 'emulators',
    'stable': 'stable'  # change it to stable when the image is ready to release.
    }

def MakeGcrTags(label_without_tag,
                label_with_tag,
                maybe_hypen,
                include_old_name=True,
                include_rebrand_name=True):
    t = []
    for gcr_prefix, gcr_suffix in GCR_PREFIXES:
        if include_old_name:
            t.append(
                '\'{gcrprefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:{label}\''
                .format(gcrprefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        gcrio_suffix=gcr_suffix,
                        old_name=OLD_NAME,
                        label=label_without_tag))
            t.append(
                '\'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:$TAG_NAME{maybe_hypen}{label}\''
                .format(gcr_prefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        old_name=OLD_NAME,
                        gcrio_suffix=gcr_suffix,
                        maybe_hypen=maybe_hypen,
                        label=label_with_tag))
            t.append(
                '\'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:$TAG_NAME{maybe_hypen}{label}-$_DATE\''
                .format(gcr_prefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        old_name=OLD_NAME,
                        gcrio_suffix=gcr_suffix,
                        maybe_hypen=maybe_hypen,
                        label=label_with_tag))
        if include_rebrand_name:
            t.append(
                '\'{gcrprefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:{label}\''
                .format(gcrprefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        gcrio_suffix=gcr_suffix,
                        rebrand_name=REBRAND_NAME,
                        label=label_without_tag))
            t.append(
                '\'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hypen}{label}\''
                .format(gcr_prefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        rebrand_name=REBRAND_NAME,
                        gcrio_suffix=gcr_suffix,
                        maybe_hypen=maybe_hypen,
                        label=label_with_tag))
            t.append(
                '\'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hypen}{label}-$_DATE\''
                .format(gcr_prefix=gcr_prefix,
                        gcrio_project=GCRIO_PROJECT,
                        rebrand_name=REBRAND_NAME,
                        gcrio_suffix=gcr_suffix,
                        maybe_hypen=maybe_hypen,
                        label=label_with_tag))
    return t

# Make all the tags and save them
tags={}
multi_arch_tags={}
for i in IMAGES:
    tags[i]=[]
    if i in MULTI_ARCH:
        multi_arch_tags[i]=[]
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
    if i not in MULTI_ARCH:
        tags[i].extend(MakeGcrTags(label_without_tag, label_with_tag, maybe_hypen))
    else:
        # old gcr tags go into tags
        tags[i].extend(MakeGcrTags(label_without_tag,
                                   label_with_tag,
                                   maybe_hypen,
                                   include_rebrand_name=False))
        # new gcr tags go into multiarch tags
        multi_arch_tags[i].extend(MakeGcrTags(label_without_tag,
                                           label_with_tag,
                                           maybe_hypen,
                                           include_old_name=False))

build_steps=''
for i in IMAGES:
    image_directory = '{}/'.format(i)
    if i == 'default':
        image_directory = '.'

    build_step = """- name: 'gcr.io/cloud-builders/docker'
  id: {image_name}
  args: ['build', '--build-arg', 'CLOUD_SDK_VERSION=$_CLI_VERSION', {tags}, '{image_directory}']
  waitFor: ['-']"""
    output_build_step = build_step.format(
        image_name=i,
        tags=', '.join(['\'-t\', {}'.format(t) for t in tags[i]]),
        image_directory=image_directory)
    if len(build_steps) > 0:
        build_steps+='\n'
    build_steps+=output_build_step

multi_arch_build_steps=''
for i in MULTI_ARCH:
    image_directory = '{}/'.format(i)
    if i == 'default':
        image_directory = '.'

    multi_arch_build_step = """- name: 'gcr.io/cloud-builders/docker'
  id: multi_arch_{image_name}
  args: ['buildx', 'build', '--build-arg', 'CLOUD_SDK_VERSION=$_CLI_VERSION', '--platform', 'linux/arm64,linux/amd64', {tags}, '{image_directory}', '--push']
  waitFor: ['multi_arch_step3']"""
    output_build_step = multi_arch_build_step.format(
        image_name=i,
        tags=', '.join(['\'-t\', {}'.format(t) for t in multi_arch_tags[i]]),
        image_directory=image_directory)
    if len(multi_arch_build_steps) > 0:
        multi_arch_build_steps+='\n'
    multi_arch_build_steps+=output_build_step

docker_push_steps=''
for i in IMAGES:
    push_step = """- name: 'gcr.io/cloud-builders/docker'
  args: ['push', {tag}]
  waitFor: ['dockersecret', '{build_step}']"""
    for tag in tags[i]:
        if tag.startswith('\'google/cloud-sdk'):
            if len(docker_push_steps) > 0:
                docker_push_steps+='\n'
            docker_push_steps+=push_step.format(tag=tag, build_step=i)

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
    MULTIARCH_BUILDSTEPS=multi_arch_build_steps,
    DOCKER_PUSHSTEPS=docker_push_steps,
    GCR_IO_TAGS_SORTED=all_gcr_io_tags_for_images
    ))
