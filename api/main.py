from patho_predictor import run

if __name__ == '__main__':
    run('./models/random_forest.joblib', './test_samples/demo.fna', './output')