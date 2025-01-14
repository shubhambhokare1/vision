from typing import Any, Optional, Dict

import torch

from ._transform import Transform


class Compose(Transform):
    def __init__(self, *transforms: Transform):
        super().__init__()
        self.transforms = transforms
        for idx, transform in enumerate(transforms):
            self.add_module(str(idx), transform)

    def forward(self, *inputs: Any) -> Any:  # type: ignore[override]
        sample = inputs if len(inputs) > 1 else inputs[0]
        for transform in self.transforms:
            sample = transform(sample)
        return sample


class RandomApply(Transform):
    def __init__(self, transform: Transform, *, p: float = 0.5) -> None:
        super().__init__()
        self.transform = transform
        self.p = p

    def forward(self, *inputs: Any, params: Optional[Dict[str, Any]] = None) -> Any:
        sample = inputs if len(inputs) > 1 else inputs[0]
        if float(torch.rand(())) < self.p:
            return sample

        return self.transform(sample, params=params)

    def extra_repr(self) -> str:
        return f"p={self.p}"


class RandomChoice(Transform):
    def __init__(self, *transforms: Transform):
        super().__init__()
        self.transforms = transforms
        for idx, transform in enumerate(transforms):
            self.add_module(str(idx), transform)

    def forward(self, *inputs: Any) -> Any:  # type: ignore[override]
        idx = int(torch.randint(len(self.transforms), size=()))
        transform = self.transforms[idx]
        return transform(*inputs)


class RandomOrder(Transform):
    def __init__(self, *transforms: Transform):
        super().__init__()
        self.transforms = transforms
        for idx, transform in enumerate(transforms):
            self.add_module(str(idx), transform)

    def forward(self, *inputs: Any) -> Any:  # type: ignore[override]
        for idx in torch.randperm(len(self.transforms)):
            transform = self.transforms[idx]
            inputs = transform(*inputs)
        return inputs
