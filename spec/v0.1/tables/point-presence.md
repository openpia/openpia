# A55a point-type presence by job-type scenario

Row keys are presence scenarios, not the jobType enum: some job types split by topology (e.g. new_box_path vs new_box_point).

| job-type scenario | start_point | end_point | item_point | blockage_point | location_point |
| --- | --- | --- | --- | --- | --- |
| blockage | required | required |  | required |  |
| desilt | required | required |  |  |  |
| pole_bend | required | required |  | required |  |
| new_track | required | required |  |  |  |
| new_box_path | required | required | required |  |  |
| new_box_point |  |  | required |  |  |
| tree_cutting_path | required | required |  |  |  |
| tree_cutting_point |  |  | required |  |  |
| chamber_capacity |  |  | required |  |  |
| pole_top_capacity |  |  | required |  |  |
| d_pole |  |  | required |  |  |
| frame_cover_replacement |  |  | required |  |  |
| gully_suck |  |  | required |  |  |
| traffic_management |  |  |  |  | required |
| new_pole |  |  | required |  |  |
