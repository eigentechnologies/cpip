# cpip

## What is it?
This tool creates a `conda` environment, with `pip` dependencies,
in any desired location, or packages it into a portable tarball. 

## How does it work?
1. Assembles an environment with basic `conda` commands from
given `conda` environment files
1. Installs cross-compilers and downloads/compiles `pip` packages
1. Packages `conda` environment via `conda-pack` tool
1. Unpacks environment to desired location (optional with `create` command)

## Supported Operating Systems
- Linux
- macOS

## System Requirements
- [conda](https://conda.io/docs/)
- [poetry](https://poetry.eustace.io/docs/) (optional)

## Environment Dependencies
- [conda-pack](https://conda.github.io/conda-pack/) (installed via `conda`)
- [jq](https://stedolan.github.io/jq/) (installed via `conda`)

## Usage

#### 1) Create Build Environment
`conda env create -f cpip`

#### 2) Activate Build Environment
`conda activate cpip`

#### 3) Run 'cpip pack' or 'cpip create'
For more information: `cpip pack --help` or `cpip create --help`

#### 4) Unpack and Activate
    Initial Setup (if using 'cpip pack'):
      1. untar archive        --> tar -xf <archive>
      2. activate environment --> source <root-dir>/bin/activate
      3. fix path prefixes    --> conda-unpack
    
    Normal Use:
      *  activate             --> source <root-dir>/bin/activate
      *  deactivate           --> source deactivate

    Info:
      *  conda dependencies     @ <archive-root>/dependencies/<archive-name>.yml
      *  poetry lockfile        @ <archive-root>/dependencies/poetry.lock

## Cleaning Caches
Use `cpip clean` command to clean the conda and/or pip caches

## Other Things to Note

#### Conda Configuration
The only change made to the configuration is that `defaults`
is removed from the `channels` key in order to enforce better
consistency. Changing other settings may yield unexpected results.

#### Poetry Configuration
`cpip pack` internally sets `settings.virtualenvs.create` to `false`,
but restores the setting to its original value upon failure.

#### Installing pip dependencies with Conda vs. Poetry
`pip` dependencies can be installed via `conda` or `poetry`.
It is recommended to use a `poetry` project to define all the `pip`
packages in your project; this allows for lockfiles to pin package
versions properly. If you decide to use `poetry`, it makes sense to
move ALL `pip` dependencies from the `conda` environment `.yml` files
to a `poetry` project `.toml` file.

#### Cross-Compilers
Cross-compilers will be installed for if any `pip` dependencies are
detected. After installing all the `pip` dependencies, the compilers
will be removed but the associated libraries will remain for the
final package. If any libraries were in the environment before,
they will be replaced, and potentially with different versions.

#### Order of Environments
This tool can take more than one `conda` environment file.
These files will be loaded in the order they are given on
the command line. Different command line orders may produce
slightly different environments.

#### Concurrency
Multiple `cpip` processes can be run concurrently if we do the following:
- if not using a `poetry` lockfile, use seperate `poetry` project directories
- create a build environment for each process, i.e. for process `X`
  1. `conda env create -n cpip-X -f cpip.yml`
  1. `conda env activate cpip-X`

##### TODO: Non-Unix Systems
For systems that don't respect the `XDG_CACHE_HOME` environment variable,
Poetry may have concurrency issues, however, if using a `poetry.lock` file,
this will relieve any potential cache conflicts.

The cache issues can be solved completely if `poetry` allows for the
something more flexible like a `--poetry-cache-dir` command line option.
