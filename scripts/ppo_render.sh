python train.py env=hopper alg=ppo general.run_wandb=False  general.render=True alg.params.config.max_epochs=5032 env.ppo.num_actors=1 alg.params.load_checkpoint=True general.checkpoint="/home/ignat/git/SHAC/scripts/runs/df_anymal_ppo_21-22-00-59/nn/last_df_anymal_ppo_ep_1500_rew_3977.4736.pth" env.config.stochastic_init=False env.ppo.minibatch_size=8 general.train=False alg.params.config.player.games_num=1 alg.params.config.player.num_actors=1