# cpip

## What is it?
This tool creates a `conda` environment and packages it into
a portable tarball, including its `pip` dependencies.

## How does it work?
1. Assembles an environment with basic `conda` commands from
given `conda` environment files
1. Installs cross-compilers and downloads/compiles `pip` packages
1. Packages `conda` environment via `conda-pack` tool

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

#### 3) Run 'cpip pack'
                usage: cpip pack --name PROJECT --file FILE [--file FILE]...
                                 [--poetry DIR] [--version VERSION] [--output DIR]
                                 [--no-dev] [--unlock] [--force] [--quiet]
                                 [--help]
               
                Package all dependencies into a portable conda environment tarball
               
                required arguments:
                  --name, -n PROJECT        Name of the project to package. Will be used for
                                            the name in the output file.
                  --file, -f FILE           Conda environment file. This option can be used
                                            multiple times to specify multiple files. The
                                            environment will be updated in the order that they
                                            are given on the command line.
               
                optional arguments:
                  --poetry, -p DIR          Poetry project directory.
                  --version, -v VERSION     Version number to be included in output file name.
                  --output, -o DIR          Directory where the final tarball will go.
                                            Otherwise, tarball will be ouputed to the current
                                            working directory.
                  --no-dev                  Do not install dev dependencies for Poetry.
                  --unlock                  Overwrite Poetry lockfile and update dependencies.
                  --force                   Overwrite any existing archive at the output path.
                  --quiet, -q               Suppress output for commands.
                  --help, -h                Show this help message then exit.

#### 4) Unpack and Activate
                Initial Setup:
                  1. untar archive        --> tar -xf <archive>
                  2. activate environment --> source <archive-root>/bin/activate
                  3. fix path prefixes    --> conda unpack
                
                Normal Use:
                  *  activate             --> source <archive-root>/bin/activate
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
final package.

**NOTE:** If you have any `pip` dependencies AND any cross-compilers
defined in your environment files, the cross-compilers will be removed
regardless of the fact you defined them to be there. Defining all `pip`
dependencies via `poetry` will prevent this from happening. Although,
its questionable why one would want to ship cross-compilers with a
portable environment in the first place.

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
