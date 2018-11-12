def add_a2c_args(parser):
    parser.add_argument('--seed', type=int, default=None,
                        help='seed to make random number sequence in the alorightm reproducible. By default is None which means seed from system noise generator (not reproducible')
    parser.add_argument('--nsteps', type=int, default=5,
                        help='int, number of steps of the vectorized environment per update (i.e. batch size is nsteps * nenv where'
                             'nenv is number of environment copies simulated in parallel)')
    parser.add_argument('--total_timesteps', type=int, default=100000,
                        help='int, total number of timesteps to train on (default: 100K')
    parser.add_argument('--log_interval', type=int, default=100,
                        help='int, specifies how frequently the logs are printed out (default: 100)')

    parser.add_argument('--lrschedule', type=str, default='linear',
                        help="schedule of learning rate. Can be 'linear', 'constant', or a function [0..1] -> [0..1] that takes fraction of the training progress as input and"
                             "returns fraction of the learning rate (specified as lr) as output")
    parser.add_argument('--vf_coef', type=float, default=0.5,
                        help='float, coefficient in front of value function loss in the total loss function (default: 0.5)')
    parser.add_argument('--ent_coef', type=float, default=0.01,
                        help='float, coeffictiant in front of the policy entropy in the total loss function (default: 0.01)')
    parser.add_argument('--max_grad_norm', type=float, default=0.5,
                        help='float, gradient is clipped to have global L2 norm no more than this value (default: 0.5)')
    parser.add_argument('--lr', type=float, default=7e-4,
                        help='float, learning rate for RMSProp (current implementation has RMSProp hardcoded in) (default: 7e-4)')
    parser.add_argument('--epsilon', type=float, default=1e-5,
                        help='float, RMSProp epsilon (stabilizes square root computation in denominator of RMSProp update) (default: 1e-5)')
    parser.add_argument('--alpha', type=float, default=0.99, help='float, RMSProp decay parameter (default: 0.99)')
    parser.add_argument('--gamma', type=float, default=0.99, help='float, reward discounting parameter (default: 0.99)')
    parser.add_argument('--network', type=str, default=0.99, help="policy network architecture. Either string (mlp, lstm, lnlstm, cnn_lstm, cnn, cnn_small, conv_only - see baselines.common/models.py for full list)"
                        "specifying the standard network architecture, or a function that takes tensorflow tensor as input and returns'"
                        "tuple (output_tensor, extra_feed) where output tensor is the last network layer output, extra_feed is None for feed-forward"
                        "neural nets, and extra_feed is a dictionary describing how to feed state into the network for recurrent neural nets."
                        "See baselines.common/policies.py/lstm for more details on using recurrent nets in policies")
    return parser
