import os
import sys


MAIN_TEMPLATE = """options:
  logging: GCS_ONLY
  machineType: 'E2_HIGHCPU_32'
  env:
    - DOCKER_CLI_EXPERIMENTAL=enabled
logsBucket: 'gs://cloud-sdk-docker-build-logs'
steps:
# Pin to qemu-v10.2.3-68 for stability and security
- name: 'tonistiigi/binfmt@sha256:400a4873b838d1b89194d982c45e5fb3cda4593fbfd7e08a02e76b03b21166f0'
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
{SCANNINGSTEPS}
{MULTIARCH_BUILDSTEPS}
{TAG_AMD64_STEPS}
{DOCKER_LOGIN_STEP}
{DOCKER_PUSHSTEPS}
{IMAGES_SECTION}
{SECRETS_SECTION}
timeout: 7200s"""

GCRIO_PROJECT='google.com/cloudsdktool'
DOCKERHUB_PREFIX='google'
GCR_PREFIXES = [
    ('us-docker.pkg.dev', 'gcr.io'),
    ('us-docker.pkg.dev', 'us.gcr.io'),
    ('europe-docker.pkg.dev', 'eu.gcr.io'),
    ('asia-docker.pkg.dev', 'asia.gcr.io'),
]
SCANNING_PREFIXES = [('us-docker.pkg.dev', 'scanning')]
OLD_NAME='cloud-sdk'
REBRAND_NAME='google-cloud-cli'
IMAGES=['alpine', 'debian_slim', 'default', 'debian_component_based', 'emulators', 'stable']
MULTI_ARCH=['debian_slim', 'debian_component_based', 'alpine', 'emulators', 'stable', 'default']
SCANNING_IMAGES=['all_components']
LABEL_FOR_IMAGE={
    'alpine': 'alpine',
    'debian_slim': 'slim',
    'default': '',
    'debian_component_based': 'debian_component_based',
    'emulators': 'emulators',
    'stable': 'stable',
    'all_components': 'all_components'
    }


def generate(is_test=False):
  def MakeScanningTags(label):
    t = []
    maybe_hyphen = '-' if label != 'latest' else ''
    for gcr_prefix, gcr_suffix in SCANNING_PREFIXES:
      t.append(
          "'{gcrprefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:{label}'"
          .format(
              gcrprefix=gcr_prefix,
              gcrio_project=GCRIO_PROJECT,
              gcrio_suffix=gcr_suffix,
              rebrand_name=REBRAND_NAME,
              label=label,
          )
      )
      t.append(
          "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hyphen}{label}'"
          .format(
              gcr_prefix=gcr_prefix,
              gcrio_project=GCRIO_PROJECT,
              gcrio_suffix=gcr_suffix,
              rebrand_name=REBRAND_NAME,
              maybe_hyphen=maybe_hyphen,
              label=label,
          )
      )
      t.append(
          "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hyphen}{label}-$_DATE'"
          .format(
              gcr_prefix=gcr_prefix,
              gcrio_project=GCRIO_PROJECT,
              gcrio_suffix=gcr_suffix,
              rebrand_name=REBRAND_NAME,
              maybe_hyphen=maybe_hyphen,
              label=label,
          )
      )
    return t

  def MakeGcrTags(
      label_without_tag,
      label_with_tag,
      maybe_hyphen,
      include_old_name=True,
      include_rebrand_name=True,
  ):
    t = []
    for gcr_prefix, gcr_suffix in GCR_PREFIXES:
      if include_old_name:
        t.append(
            "'{gcrprefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:{label}'"
            .format(
                gcrprefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                gcrio_suffix=gcr_suffix,
                old_name=OLD_NAME,
                label=label_without_tag,
            )
        )
        t.append(
            "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:$TAG_NAME{maybe_hyphen}{label}'"
            .format(
                gcr_prefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                old_name=OLD_NAME,
                gcrio_suffix=gcr_suffix,
                maybe_hyphen=maybe_hyphen,
                label=label_with_tag,
            )
        )
        t.append(
            "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{old_name}:$TAG_NAME{maybe_hyphen}{label}-$_DATE'"
            .format(
                gcr_prefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                old_name=OLD_NAME,
                gcrio_suffix=gcr_suffix,
                maybe_hyphen=maybe_hyphen,
                label=label_with_tag,
            )
        )
      if include_rebrand_name:
        t.append(
            "'{gcrprefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:{label}'"
            .format(
                gcrprefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                gcrio_suffix=gcr_suffix,
                rebrand_name=REBRAND_NAME,
                label=label_without_tag,
            )
        )
        t.append(
            "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hyphen}{label}'"
            .format(
                gcr_prefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                rebrand_name=REBRAND_NAME,
                gcrio_suffix=gcr_suffix,
                maybe_hyphen=maybe_hyphen,
                label=label_with_tag,
            )
        )
        t.append(
            "'{gcr_prefix}/{gcrio_project}/{gcrio_suffix}/{rebrand_name}:$TAG_NAME{maybe_hyphen}{label}-$_DATE'"
            .format(
                gcr_prefix=gcr_prefix,
                gcrio_project=GCRIO_PROJECT,
                rebrand_name=REBRAND_NAME,
                gcrio_suffix=gcr_suffix,
                maybe_hyphen=maybe_hyphen,
                label=label_with_tag,
            )
        )
    return t

  # Make all the tags and save them
  tags = {}
  multi_arch_tags = {}
  for i in IMAGES:
    tags[i] = []
    if i in MULTI_ARCH:
      multi_arch_tags[i] = []
    label_name = LABEL_FOR_IMAGE[i]
    label_without_tag = label_name
    label_with_tag = label_name
    maybe_hyphen = '-'
    if i == 'default':
      label_without_tag = 'latest'
      maybe_hyphen = ''

    # Make dockerhub tags for i
    tags[i].append(
        "'{dockerhub_prefix}/{old_name}:{label}'".format(
            dockerhub_prefix=DOCKERHUB_PREFIX,
            old_name=OLD_NAME,
            label=label_without_tag,
        )
    )
    tags[i].append(
        "'{dockerhub_prefix}/{old_name}:$TAG_NAME{maybe_hyphen}{label}'"
        .format(
            dockerhub_prefix=DOCKERHUB_PREFIX,
            old_name=OLD_NAME,
            maybe_hyphen=maybe_hyphen,
            label=label_with_tag,
        )
    )
    # Make gcr tags for i
    if i not in MULTI_ARCH:
      tags[i].extend(
          MakeGcrTags(label_without_tag, label_with_tag, maybe_hyphen)
      )
    else:
      # old gcr tags go into tags
      tags[i].extend(
          MakeGcrTags(
              label_without_tag,
              label_with_tag,
              maybe_hyphen,
              include_rebrand_name=False,
          )
      )
      # new gcr tags go into multiarch tags
      multi_arch_tags[i].extend(
          MakeGcrTags(
              label_without_tag,
              label_with_tag,
              maybe_hyphen,
              include_old_name=False,
          )
      )
  # Make scanning tags and save them
  scanning_tags = {}
  for i in SCANNING_IMAGES:
    scanning_tags[i] = []
    label_name = LABEL_FOR_IMAGE[i]
    if i == 'default':
      label_name = 'latest'
    scanning_tags[i].extend(MakeScanningTags(label_name))

  scanning_steps = ''
  for i in SCANNING_IMAGES:
    image_directory = '{}/'.format(i)
    if i == 'default':
      image_directory = '.'

    scanning_step = """- name: 'gcr.io/cloud-builders/docker'
  id: scanning_{image_name}
  args: ['build', '--target', 'prod', '--build-arg', 'CLOUD_SDK_VERSION=$_CLI_VERSION', {scanning_tags}, '{image_directory}']
  waitFor: ['-']"""
    output_scanning_step = scanning_step.format(
        image_name=i,
        scanning_tags=', '.join(
            ["'-t', {}".format(t) for t in scanning_tags[i]]
        ),
        image_directory=image_directory,
    )
    if len(scanning_steps) > 0:
      scanning_steps += '\n'
    scanning_steps += output_scanning_step

  tag_amd64_steps = ''
  for i in IMAGES:
    image_directory = '{}/'.format(i)
    if i == 'default':
      image_directory = '.'

    if not is_test:
      primary_tag = multi_arch_tags[i][0].strip("'")
      tag_cmds = ' && '.join([
          'docker tag {} {}'.format(primary_tag, t.strip("'")) for t in tags[i]
      ])
      step_template = """- name: 'gcr.io/cloud-builders/docker'
  id: tag_amd64_{image_name}
  entrypoint: 'bash'
  args: ['-c', 'docker pull {primary_tag} && {tag_cmds}']
  waitFor: ['multi_arch_{image_name}']"""
      output_step = step_template.format(
          image_name=i,
          primary_tag=primary_tag,
          tag_cmds=tag_cmds,
      )
    else:
      target_flag = "'--target', 'prod', " if i == 'alpine' else ''
      step_template = """- name: 'gcr.io/cloud-builders/docker'
  id: tag_amd64_{image_name}
  args: ['buildx', 'build', {target_flag}'--build-arg', 'CLOUD_SDK_VERSION=$_CLI_VERSION', '--platform', 'linux/amd64', '--load', {tags}, '{image_directory}']
  waitFor: ['multi_arch_{image_name}']"""
      output_step = step_template.format(
          image_name=i,
          target_flag=target_flag,
          tags=', '.join(["'-t', {}".format(t) for t in tags[i]]),
          image_directory=image_directory,
      )
    if len(tag_amd64_steps) > 0:
      tag_amd64_steps += '\n'
    tag_amd64_steps += output_step

  multi_arch_build_steps = ''
  push_flag = ", '--push'" if not is_test else ''
  for i in MULTI_ARCH:
    image_directory = '{}/'.format(i)
    if i == 'default':
      image_directory = '.'

    target_flag = "'--target', 'prod', " if i == 'alpine' else ''
    multi_arch_build_step = """- name: 'gcr.io/cloud-builders/docker'
  id: multi_arch_{image_name}
  args: ['buildx', 'build', {target_flag}'--build-arg', 'CLOUD_SDK_VERSION=$_CLI_VERSION', '--platform', 'linux/arm64,linux/amd64', {tags}, '{image_directory}'{push_flag}]
  waitFor: ['multi_arch_step3']"""
    output_build_step = multi_arch_build_step.format(
        image_name=i,
        target_flag=target_flag,
        tags=', '.join(["'-t', {}".format(t) for t in multi_arch_tags[i]]),
        image_directory=image_directory,
        push_flag=push_flag,
    )
    if len(multi_arch_build_steps) > 0:
      multi_arch_build_steps += '\n'
    multi_arch_build_steps += output_build_step

  docker_push_steps = ''
  if not is_test:
    for i in IMAGES:
      push_step = """- name: 'gcr.io/cloud-builders/docker'
  args: ['push', {tag}]
  waitFor: ['dockersecret', '{build_step}']"""
      for tag in tags[i]:
        if tag.startswith("'google/cloud-sdk"):
          if len(docker_push_steps) > 0:
            docker_push_steps += '\n'
          docker_push_steps += push_step.format(tag=tag, build_step='tag_amd64_' + i)

  docker_login_step = ''
  if not is_test:
    docker_login_step = """- name: 'gcr.io/cloud-builders/docker'
  id: dockersecret
  entrypoint: 'bash'
  args: ['-c', 'docker login --username=$_USERNAME --password=$$PASSWORD']
  secretEnv: ['PASSWORD']"""

  all_gcr_io_tags_for_images = ''
  images_section = ''
  if not is_test:
    all_images_tags = []
    for i in IMAGES:
      all_images_tags.extend(
          [t for t in tags[i] if not t.startswith("'google/cloud-sdk")]
      )
    for i in SCANNING_IMAGES:
      all_images_tags.extend(t for t in scanning_tags[i])
    for tag in sorted(all_images_tags):
      if len(all_gcr_io_tags_for_images) > 0:
        all_gcr_io_tags_for_images += '\n'
      all_gcr_io_tags_for_images += '- {}'.format(tag)
    images_section = 'images:\n' + all_gcr_io_tags_for_images

  secrets_section = ''
  if not is_test:
    secrets_section = """secrets:
- kmsKeyName: projects/google.com:cloudsdktool/locations/global/keyRings/docker/cryptoKeys/dockerhub-password
  secretEnv:
    PASSWORD: |
        CiQA9btlfpg/kWmwXQvrNXtkVpu2tDdD2VOi1FYd3mmjCUGaK4YSNwC8sn1MepjracHAg8VAQEWm
        s26BTGccqD1NTS83DGFdY9moRGhSPm4WJKCg2tTQKYeTfdqUjjM="""

  return MAIN_TEMPLATE.format(
      SCANNINGSTEPS=scanning_steps,
      MULTIARCH_BUILDSTEPS=multi_arch_build_steps,
      TAG_AMD64_STEPS=tag_amd64_steps,
      DOCKER_LOGIN_STEP=docker_login_step,
      DOCKER_PUSHSTEPS=docker_push_steps,
      IMAGES_SECTION=images_section,
      SECRETS_SECTION=secrets_section,
  )


def main():
  workspace_dir = os.environ.get('BUILD_WORKSPACE_DIRECTORY')
  if workspace_dir:
    yaml_file = os.path.join(
        workspace_dir,
        'third_party/gcloud_cli/external/cloud_sdk_docker/cloudbuild.yaml',
    )
    test_yaml_file = os.path.join(
        workspace_dir,
        'third_party/gcloud_cli/external/cloud_sdk_docker/cloudbuild_test.yaml',
    )

    # Generate cloudbuild.yaml
    with open(yaml_file, 'w') as f:
      f.write(generate(is_test=False) + '\n')

    # Generate cloudbuild_test.yaml
    with open(test_yaml_file, 'w') as f:
      f.write(
          '# IT IS A TEST\n' + generate(is_test=True) + '\n'
      )

    print('Successfully updated all cloudbuild yaml files.')
  else:
    is_test = 'is_test' in sys.argv
    if is_test:
      print('# IT IS A TEST')
    print(generate(is_test=is_test))


if __name__ == '__main__':
  main()
