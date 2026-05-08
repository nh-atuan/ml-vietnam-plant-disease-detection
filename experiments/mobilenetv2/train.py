"""
MobileNetV2 Training Entry Point.

Phụ trách: Lê Xuân Trí
Phase 3, Task 3.4

Cách chạy:
    python experiments/mobilenetv2/train.py --config configs/models/mobilenetv2.yaml

TODO:
- [ ] Load config (merge training_defaults + mobilenetv2.yaml)
- [ ] Khởi tạo model MobileNetV2 từ ModelFactory
- [ ] Khởi tạo DataLoader từ data splits
- [ ] Khởi tạo BaseTrainer với callbacks
- [ ] Chạy trainer.fit()
- [ ] Log kết quả cuối cùng
"""

import argparse
import sys
import os

# Thêm project root vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


def parse_args():
    parser = argparse.ArgumentParser(description="Train MobileNetV2")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/models/mobilenetv2.yaml",
        help="Path to model config YAML",
    )
    parser.add_argument(
        "--resume",
        type=str,
        default=None,
        help="Path to checkpoint to resume from",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # TODO: Load and merge configs
    # config = load_config(args.config, defaults="configs/training_defaults.yaml")

    # TODO: Setup data loaders
    # train_loader, val_loader = create_dataloaders(config)

    # TODO: Create model
    # model = ModelFactory.create("mobilenetv2", num_classes=config.num_classes)

    # TODO: Setup optimizer, scheduler, criterion
    # optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    # scheduler = CosineAnnealingLR(optimizer, T_max=config.epochs)
    # criterion = nn.CrossEntropyLoss(weight=class_weights)

    # TODO: Setup callbacks
    # callbacks = [EarlyStopping(...), ModelCheckpoint(...), MLflowLogger(...)]

    # TODO: Create trainer and train
    # trainer = BaseTrainer(model, train_loader, val_loader, optimizer, ...)
    # history = trainer.fit(num_epochs=config.epochs)

    print("MobileNetV2 training — TODO: implement")


if __name__ == "__main__":
    main()
