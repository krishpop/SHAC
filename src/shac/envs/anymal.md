# Tuning anymal

### micro experiment 0 - removing height reward



## setup #1
```
lu.urdf_load(
    self.builder,
    os.path.join(asset_folder, filename),
    df.transform(
        start_pos,
        self.start_rot,
    ),
    robot=robot,
    floating=True,
    stiffness=85.0,  # from config
    damping=2.0,  # from config
    shape_ke=2.0e3,
    shape_kd=1.0e2,
    shape_kf=1.0e2,
    shape_mu=0.5,
    limit_ke=1.0e3,
    limit_kd=1.0e1,
    armature=0.006,
)
```

- PPO gets ~12k reward. SHAC gets ~15k rewards.
- SHAC is somewhat unstable
- Robot clips inside


## setup #2 - higher mu aligned with other envs

```
lu.urdf_load(
    self.builder,
    os.path.join(asset_folder, filename),
    df.transform(
        start_pos,
        self.start_rot,
    ),
    robot=robot,
    floating=True,
    stiffness=85.0,  # from config
    damping=2.0,  # from config
    shape_ke=2.0e3,
    shape_kd=1.0e2,
    shape_kf=1.0e2,
    shape_mu=0.75,
    limit_ke=1.0e3,
    limit_kd=1.0e1,
    armature=0.006,
)
```

- SHAC seems to be performing well (if not better than before)
- Still about the same amount of clipping :(

## Setup #3 - kd, kf aligned with humanoid relative values

```
lu.urdf_load(
    self.builder,
    os.path.join(asset_folder, filename),
    df.transform(
        start_pos,
        self.start_rot,
    ),
    robot=robot,
    floating=True,
    stiffness=85.0,  # from config
    damping=2.0,  # from config
    shape_ke=2.0e3,
    shape_kd=5.0e2,
    shape_kf=1.0e2,
    shape_mu=0.75,
    limit_ke=1.0e3,
    limit_kd=1.0e1,
    armature=0.006,
)
```

- SHAC still works well. Outperforms PPO by a huge margin actually!
- Less clipping but still a decent amount

## Setup #4 - even stiffer contact

```
lu.urdf_load(
    self.builder,
    os.path.join(asset_folder, filename),
    df.transform(
        start_pos,
        self.start_rot,
    ),
    robot=robot,
    floating=True,
    stiffness=85.0,  # from config
    damping=2.0,  # from config
    shape_ke=4.0e3,
    shape_kd=1.0e3,
    shape_kf=2.0e2,
    shape_mu=0.75,
    limit_ke=1.0e3,
    limit_kd=1.0e1,
    armature=0.006,
)
```

- even less clipping. Looks quite nice
- SHAC doesn't perform as well with 64 envs
- Need to figure out if it can be improved

## Setup #5 - even more stiffer contact

```
lu.urdf_load(
    self.builder,
    os.path.join(asset_folder, filename),
    df.transform(
        start_pos,
        self.start_rot,
    ),
    robot=robot,
    floating=True,
    stiffness=85.0,  # from config
    damping=2.0,  # from config
    shape_ke=8.0e3,
    shape_kd=2.0e3,
    shape_kf=4.0e2,
    shape_mu=0.75,
    limit_ke=1.0e3,
    limit_kd=1.0e1,
    armature=0.006,
)
```
- ehh clipping doesn't look that good tbh

### SHAC specific tuning
- The more envs, the better things work! 128,256 work the best