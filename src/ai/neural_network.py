import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os


class NeuralNetwork:
    def __init__(self):
        self.logarithmic_base = 1.5
        self.model = None
        self.input_size = 272
        self.output_size = 272
        self.model_path = "game_model.keras"  # Changed extension to .keras

    def create_model(self):
        """Create a new neural network model. Input 272 nodes, output 272"""
        self.model = Sequential(
            [
                # Input layer
                Dense(544, activation="relu", input_shape=(self.input_size,)),
                Dropout(0.2),
                # Hidden layers
                Dense(272, activation="relu"),
                Dropout(0.2),
                Dense(136, activation="relu"),
                Dense(272, activation="relu"),
                # Output layer - using sigmoid to get values between 0 and 1
                Dense(self.output_size, activation="sigmoid"),
            ]
        )

        self.model.compile(
            optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["accuracy"]
        )

        return self.model

    def load_model(self):
        """Load a pre-trained model"""
        if os.path.exists(self.model_path):
            try:
                self.model = load_model(self.model_path)
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False

    def save_model(self):
        """Save the current model"""
        if self.model is not None:
            try:
                self.model.save(self.model_path)  # Using native Keras format
                return True
            except Exception as e:
                print(f"Error saving model: {e}")
                return False
        return False

    def evaluate(self, input_layer):
        """Evaluate the input layer"""
        if self.model is None:
            self.create_model()

        # Convert input to numpy array and reshape
        input_array = np.array(input_layer).reshape(1, -1)

        # Get model predictions
        predictions = self.model.predict(input_array, verbose=0)
        output_layer = predictions[0].tolist()

        print(
            "Input layer (min, median, max):",
            [min(input_layer), int(np.median(input_layer)), max(input_layer)],
        )
        print(
            "Output layer (min, median, max):",
            [min(output_layer), float(np.median(output_layer)), max(output_layer)],
        )

        return output_layer

    def scale_reward(self, reward, max_value=272):
        """
        Scale the reward using configurable logarithmic base, handling positive, negative, and zero values.
        """
        reward = reward - 1
        if reward == 0:
            return 0

        sign = np.sign(reward)
        abs_reward = abs(reward)
        scaled = np.log(abs_reward + 1) / np.log(self.logarithmic_base)
        normalized = scaled / (np.log(max_value + 1) / np.log(self.logarithmic_base))

        return sign * normalized

    def learn(self, input_layer, output_layer, reward):
        """Train the model with the input and output layer"""
        if self.model is None:
            self.create_model()

        # Scale the reward
        scaled_reward = self.scale_reward(reward)

        # Prepare input data
        X = np.array(input_layer).reshape(1, -1)

        # Scale the output layer by the reward
        # If reward is positive, we want to encourage these moves
        # If reward is negative, we want to discourage these moves
        scaled_output = np.array(output_layer) * (1 + scaled_reward)
        # Clip values to ensure they stay between 0 and 1
        scaled_output = np.clip(scaled_output, 0, 1)
        y = scaled_output.reshape(1, -1)

        # Train the model for one epoch
        history = self.model.fit(X, y, epochs=1, verbose=0)

        # save the model after training
        self.save_model()

        return scaled_reward

    def get_model_summary(self):
        """Return a string representation of the model architecture"""
        if self.model is None:
            self.create_model()

        # Create a string buffer to capture the summary
        from io import StringIO

        buffer = StringIO()
        self.model.summary(print_fn=lambda x: buffer.write(x + "\n"))
        return buffer.getvalue()
