### HIGH PRIORTY:
- switch `--unlock` option to use `poetry update`
- make new command `create` which unpacks and
  fixes prefixes
- new option `--post-install`;
  allows scripts to execute WITHIN build env
- organize folders into `bin` and `src`
- use `jq` inplace of `grep` for `conda` outputs
- improve logging output
  - pass i.e. `--log-quiet` option only to `conda` and `pip` (not `poetry`)
  - pipe stdout and stderr different places
### LOW PRIORITY:
- pickup progress bar from `install_cross_compilers`
- add `Python` and `pip` if not in `conda` environment
