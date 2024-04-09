# `entities-service`

Entities Service utility CLI

**Usage**:

```console
$ entities-service [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show version and exit.
* `--dotenv-config FILE`: Use the .env file at the given location for the current command. By default it will point to the .env file in the current directory.  [default: /home/cwa/venv/entities-service/entities-service/.env]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `config`: Manage configuration options.
* `login`: Login to the entities service.
* `upload`: Upload (local) entities to a remote location.

## `entities-service config`

Manage configuration options.

**Usage**:

```console
$ entities-service config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show version and exit.
* `--dotenv-config FILE`: Use the .env file at the given location for the current command. By default it will point to the .env file in the current directory.  [default: /home/cwa/venv/entities-service/entities-service/.env]
* `--help`: Show this message and exit.

**Commands**:

* `set`: Set a configuration option.
* `show`: Show the current configuration.
* `unset`: Unset a single configuration option.
* `unset-all`: Unset all configuration options.

### `entities-service config set`

Set a configuration option.

**Usage**:

```console
$ entities-service config set [OPTIONS] KEY:{access_token|backend|base_url|ca_file|debug|mongo_collection|mongo_db|mongo_password|mongo_uri|mongo_user|oauth2_provider|oauth2_provider_base_url|roles_group|x509_certificate_file} [VALUE]
```

**Arguments**:

* `KEY:{access_token|backend|base_url|ca_file|debug|mongo_collection|mongo_db|mongo_password|mongo_uri|mongo_user|oauth2_provider|oauth2_provider_base_url|roles_group|x509_certificate_file}`: Configuration option to set. These can also be set as an environment variable by prefixing with 'ENTITIES_SERVICE_'.  [required]
* `[VALUE]`: Value to set. This will be prompted for if not provided.

**Options**:

* `--help`: Show this message and exit.

### `entities-service config show`

Show the current configuration.

**Usage**:

```console
$ entities-service config show [OPTIONS]
```

**Options**:

* `--reveal-sensitive`: Reveal sensitive values. (DANGEROUS! Use with caution.)
* `--help`: Show this message and exit.

### `entities-service config unset`

Unset a single configuration option.

**Usage**:

```console
$ entities-service config unset [OPTIONS] KEY:{access_token|backend|base_url|ca_file|debug|mongo_collection|mongo_db|mongo_password|mongo_uri|mongo_user|oauth2_provider|oauth2_provider_base_url|roles_group|x509_certificate_file}
```

**Arguments**:

* `KEY:{access_token|backend|base_url|ca_file|debug|mongo_collection|mongo_db|mongo_password|mongo_uri|mongo_user|oauth2_provider|oauth2_provider_base_url|roles_group|x509_certificate_file}`: Configuration option to unset.  [required]

**Options**:

* `--help`: Show this message and exit.

### `entities-service config unset-all`

Unset all configuration options.

**Usage**:

```console
$ entities-service config unset-all [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `entities-service login`

Login to the entities service.

**Usage**:

```console
$ entities-service login [OPTIONS]
```

**Options**:

* `-q, -s, -y, --quiet, --silent`: Do not print anything on success and do not ask for confirmation.
* `--help`: Show this message and exit.

## `entities-service upload`

Upload (local) entities to a remote location.

**Usage**:

```console
$ entities-service upload [OPTIONS]
```

**Options**:

* `-f, --file FILE`: Path to file with one or more entities.
* `-d, --dir DIRECTORY`: Path to directory with files that include one or more entities. All files matching the given format(s) in the directory will be uploaded. Subdirectories will be ignored. This option can be provided multiple times, e.g., to include multiple subdirectories.
* `--format [json|yaml|yml]`: Format of entity file(s).  [default: json]
* `--fail-fast`: Stop uploading entities on the first error during file validation.
* `-q, -s, -y, --quiet, --silent`: Do not print anything on success and do not ask for confirmation. IMPORTANT, for content conflicts the defaults will be chosen.
* `--help`: Show this message and exit.