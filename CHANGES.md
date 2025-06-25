# Changes summary

To get a quick overview of what must be changed, these are the changelog (as of 25 June 2025).

Changes on the `script/` and `Dockerfile` (in `docker/pravega`): 

- `Dockerfile`: basically change the base image, fix the path, and fetch binaries/releases from github.
- `entrypoint.sh`: there was some error using `sh` instead of `bash`. To be honest I don't think this is necessary. Could be omitted.
- `init_*.sh`: Especially in _segmentstore_, there was some error regarding cache size exceeding VM size. Here I added `add_system_property "pravegaservice.cache.size.max" "429496729"`. The number could be anything sensible, I guess. Using SCONE prevents application to peek into many `/proc`s, therefore some incorrect metrics might be used to measure the memory.

Changes on the `docker-compose-nfs.yml`: 
- Refer correct images
- Removing existing HDFS mentions, we don't need that anyway.
- Remove NFS driver on docker. To emulate Tier 2 storage, we're using local docker volume instead.
- Not sure what's `$HOST_IP` for, changing it to controller/segmentstore instead.
- Add cache limit to segmentstore service. See above.
- Always restart if fail. Somehow the sconfied version got a segfault. Especially the controller.

