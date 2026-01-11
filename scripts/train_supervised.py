from training.supervised_trainer import SupervisedTrainer

def main():
    trainer = SupervisedTrainer()
    trainer.train(
        pgn_path="data/raw/games.pgn",
        epochs=1
    )

if __name__ == "__main__":
    main()