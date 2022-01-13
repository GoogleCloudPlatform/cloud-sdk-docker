MAIN_TEMPLATE="""# PROD BUILDING STEPS
options:
  machineType: 'E2_HIGHCPU_32'
steps:
{BUILDSTEPS}
# END OF PROD BUILDING STEPS
- name: 'gcr.io/cloud-builders/docker'
  id: dockersecret
  entrypoint: 'bash'
  args: ['-c', 'docker login --username=$_USERNAME --password=$$PASSWORD']
  secretEnv: ['PASSWORD']
{PUSHSTEPS}
## Rebrand google-cloud-cli public steps
{REBRAND_TAG_STEPS}
images:
{REBRAND_IMAGE_TAGS_SORTED}
secrets:
- kmsKeyName: projects/google.com:cloudsdktool/locations/global/keyRings/docker/cryptoKeys/dockerhub-password
  secretEnv:
    PASSWORD: |
        CiQA9btlfpg/kWmwXQvrNXtkVpu2tDdD2VOi1FYd3mmjCUGaK4YSNwC8sn1MepjracHAg8VAQEWm
        s26BTGccqD1NTS83DGFdY9moRGhSPm4WJKCg2tTQKYeTfdqUjjM=
timeout: 7200s"""

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
rebrand_tags={}
for i in IMAGES:
    tags[i]=[]
    rebrand_tags[i]=[]
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
        rebrand_tags[i].append(
            '\'{gcrprefix}/{gcrio_project}/{rebrand_name}:{label}\''
            .format(gcrprefix=gcr_prefix,
                    gcrio_project=GCRIO_PROJECT,
                    rebrand_name=REBRAND_NAME,
                    label=label_without_tag))
        rebrand_tags[i].append(
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
  args: ['build', {tags}, '{image_directory}']
  waitFor: ['-']"""
    output_build_step = build_step.format(
        image_name=i,
        tags=', '.join(['\'-t\', {}'.format(t) for t in  tags[i]]),
        image_directory=image_directory)
    if len(build_steps) > 0:
        build_steps+='\n'
    build_steps+=output_build_step

push_steps=''
for i in IMAGES:
    push_step = """- name: 'gcr.io/cloud-builders/docker'
  args: ['push', {tag}]
  waitFor: ['dockersecret', '{build_step}']"""
    for tag in tags[i]:
        if tag.startswith('\'google/cloud-sdk'):
            if len(push_steps) > 0:
                push_steps+='\n'
            push_steps+=push_step.format(tag=tag, build_step=i)

rebrand_tag_steps=''
for i in IMAGES:
    rebrand_tag_step = """- name: 'gcr.io/cloud-builders/docker'
  id: {step_name_prefix}_{step_count}
  args: ['tag', {source_tag}, {rebrand_tag}]
  waitFor: ['{build_step}']"""
    step_name_prefix='google_cloud_cli_tag_{}'.format(i)
    step_count=1
    label=LABEL_FOR_IMAGE[i]
    if i == 'default':
        label = 'latest'
    source_tag='\'gcr.io/google.com/cloudsdktool/cloud-sdk:{}\''.format(label)
    for tag in rebrand_tags[i]:
        if len(rebrand_tag_steps) > 0:
            rebrand_tag_steps+='\n'
        rebrand_tag_steps+=rebrand_tag_step.format(
            step_name_prefix=step_name_prefix,
            step_count=step_count,
            source_tag=source_tag,
            rebrand_tag=tag,
            build_step=i)
        step_count+=1

all_rebranded_tags_for_images=''
all_images_tags=[]
for i in IMAGES:
    all_images_tags.extend(rebrand_tags[i])
    all_images_tags.extend([t for t in tags[i] if not t.startswith('\'google/cloud-sdk')])
for rebranded_tag in sorted(all_images_tags):
    if len(all_rebranded_tags_for_images) > 0:
        all_rebranded_tags_for_images+='\n'
    all_rebranded_tags_for_images+='- {}'.format(rebranded_tag)

print(MAIN_TEMPLATE.format(
    BUILDSTEPS=build_steps,
    PUSHSTEPS=push_steps,
    REBRAND_TAG_STEPS=rebrand_tag_steps,
    REBRAND_IMAGE_TAGS_SORTED=all_rebranded_tags_for_images
    ))
