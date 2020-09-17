import unittest

from maml.base import SKLModel, KerasModel, \
    is_sklearn_model, is_keras_model
from monty.tempfile import ScratchDir


class TestBaseModel(unittest.TestCase):

    def test_sklmodel(self):
        from sklearn.linear_model import LinearRegression
        model = SKLModel(model=LinearRegression())
        x = [[1, 2], [3, 4]]
        y = [3, 7]
        model.fit(x, y)
        model.train(x, y)
        self.assertAlmostEqual(model.predict_objs([[4, 5]])[0], 9)
        with ScratchDir("."):
            model.save("test_model.sav")
            model.fit([[1, 2], [3, 4]], [6, 14])
            self.assertAlmostEqual(model.predict_objs([[4, 5]])[0], 18)
            model.load("test_model.sav")
            self.assertAlmostEqual(model.predict_objs([[4, 5]])[0], 9)
            model2 = SKLModel.from_file("test_model.sav")
            self.assertAlmostEqual(model2.predict_objs([[4, 5]])[0], 9)
            self.assertAlmostEqual(model2.evaluate([[4, 8], [8, 5]], [12, 13]), 1.0)
        self.assertTrue(is_sklearn_model(model))
        self.assertFalse(is_keras_model(model))

    def test_keras_model(self):
        import tensorflow as tf
        import numpy as np
        model = KerasModel(model=tf.keras.Sequential([tf.keras.layers.Dense(1, input_dim=2)]))
        model.model.compile("adam", "mse")

        x = np.array([[1, 2], [3, 4]])
        y = np.array([3, 7]).reshape((-1, 1))
        model.fit(x, y)
        model.train(x, y)
        model.model.set_weights([np.array([[1.], [1.]]), np.array([0])])
        self.assertAlmostEqual(model.predict_objs([[4, 5]])[0], 9)

        with ScratchDir("."):
            model.save("test_model.sav")
            model.fit(np.array([[1, 2], [3, 4]]), np.array([6, 14])[:, None])
            model.load("test_model.sav")
            self.assertAlmostEqual(model.predict_objs([[4, 5]])[0], 9)
            model2 = KerasModel.from_file("test_model.sav")
            self.assertAlmostEqual(model2.predict_objs([[4, 5]])[0], 9)
            self.assertAlmostEqual(model2.evaluate([[4, 8], [8, 5]], [12, 13]), 0.0)
        self.assertFalse(is_sklearn_model(model))
        self.assertTrue(is_keras_model(model))


if __name__ == "__main__":
    unittest.main()