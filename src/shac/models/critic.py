# Copyright (c) 2022 NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import torch
import torch.nn as nn
import numpy as np

from shac.models import model_utils
from rl_games.algos_torch.network_builder import DoubleQCritic


def DoubleQCriticMLP(input_size, cfg_network, device="cuda:0"):
    units = cfg_network["critic_mlp"]["units"]
    activation = cfg_network["critic_mlp"]["activation"]
    critic = DoubleQCritic(
        1,
        input_size=input_size,
        units=units,
        activation=activation,
        dense_func=torch.nn.Linear,
    ).to(device)
    print(critic)
    return critic


class CriticMLP(nn.Module):
    def __init__(self, obs_dim, units, activation: str, device="cuda:0"):
        super(CriticMLP, self).__init__()

        self.device = device

        self.layer_dims = [obs_dim] + units + [1]

        init_ = lambda m: model_utils.init(
            m, nn.init.orthogonal_, lambda x: nn.init.constant_(x, 0), np.sqrt(2)
        )

        modules = []
        for i in range(len(self.layer_dims) - 1):
            modules.append(init_(nn.Linear(self.layer_dims[i], self.layer_dims[i + 1])))
            if i < len(self.layer_dims) - 2:
                modules.append(model_utils.get_activation_func(activation))
                modules.append(torch.nn.LayerNorm(self.layer_dims[i + 1]))

        self.critic = nn.Sequential(*modules).to(device)

        self.obs_dim = obs_dim

        print(self.critic)

    def forward(self, observations):
        return self.critic(observations)


class QCriticMLP(nn.Module):
    def __init__(self, input_size, units, activation: str, device="cuda:0"):
        super(QCriticMLP, self).__init__()

        self.device = device

        self.layer_dims = [input_size] + units + [1]

        init_ = lambda m: model_utils.init(
            m, nn.init.orthogonal_, lambda x: nn.init.constant_(x, 0), np.sqrt(2)
        )

        modules = []
        for i in range(len(self.layer_dims) - 1):
            modules.append(init_(nn.Linear(self.layer_dims[i], self.layer_dims[i + 1])))
            if i < len(self.layer_dims) - 2:
                modules.append(model_utils.get_activation_func(activation))
                modules.append(torch.nn.LayerNorm(self.layer_dims[i + 1]))

        self.q_function = nn.Sequential(*modules).to(device)

        print(self.q_function)

    def forward(self, observations, actions):
        return self.q_function(torch.cat([observations, actions], dim=-1))
