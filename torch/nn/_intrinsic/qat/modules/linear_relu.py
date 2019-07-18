from __future__ import absolute_import, division, print_function, unicode_literals
from torch.nn._intrisic import LinearReLU as NNLinearReLU
from torch.nn.qat import Linear as QATLinear
from torch.quantization.QConfig import default_qat_qconfig
import torch.nn.functional as F

class LinearReLU(QATLinear):
    r"""
    A linear module attached with FakeQuantize modules for both output
    activation and weight, used for quantization aware training.

    We adopt the same interface as `torch.nn.Linear`, please see https://pytorch.org/docs/stable/nn.html#torch.nn.Linear
    for documentation.

    Similar to `torch.nn._intrinsic.LinearReLU`, with FakeQuantize modules initialized to
    default.

    Attributes:
        observer: fake quant module for output activation, it's called observer
            to align with post training flow, TODO: rename?
        weight: fake quant module for weight

    Examples::

        >>> m = nn.qat.LinearReLU(20, 30)
        >>> input = torch.randn(128, 20)
        >>> output = m(input)
        >>> print(output.size())
        torch.Size([128, 30])
    """
    __constants__ = ['bias', 'in_features', 'out_features']

    def __init__(self, in_features, out_features, bias=True,
                 activation_fake_quant=default_qat_qconfig.activation(),
                 weight_fake_quant=default_qat_qconfig.weight()):
        assert bias, 'nobias is not supported in qat LinearReLU module yet'
        super(LinearReLU, self).__init__(in_features, out_features, bias, activation_fake_quant, weight_fake_quant)

    def forward(self, input):
        return self.observer(F.relu(F.linear(input, self.weight_fake_quant(self.weight), self.bias)))
