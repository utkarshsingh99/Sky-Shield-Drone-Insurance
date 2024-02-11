const fs = require('fs');
const csv = require('csv-parser');
const tf = require('@tensorflow/tfjs-node');

// Function to load data from CSV file
async function loadData(filePath) {
  const data = [];
  return new Promise((resolve, reject) => {
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (row) => {
        data.push(row);
      })
      .on('end', () => {
        resolve(data);
      })
      .on('error', (error) => {
        reject(error);
      });
  });
}

// Load data from CSV file
const filePath = 'path/to/your/data.csv';
loadData(filePath).then((data) => {
  // Process loaded data
  const processedData = data.map((row) => [
    parseFloat(row['Usage Frequency']),
    parseFloat(row['Purpose of Use']),
    parseFloat(row['Customer Satisfaction']),
    parseFloat(row['Age']),
    parseFloat(row['Obstacle Avoidance']),
    parseFloat(row['Price']),  // Including 'Price' as a feature for prediction
  ]);

  // Output data (target variable)
  const labels = data.map((row) => parseFloat(row['cluster_no']));

  // Define a simple linear regression model
  const model = tf.sequential();
  model.add(tf.layers.dense({ units: 1, inputShape: [6] }));

  // Compile the model
  model.compile({
    optimizer: 'sgd', // Stochastic Gradient Descent
    loss: 'meanSquaredError',
    metrics: ['mse'],
  });

  // Convert data to TensorFlow tensors
  const xs = tf.tensor2d(processedData);
  const ys = tf.tensor1d(labels);

  // Train the model
  model.fit(xs, ys, { epochs: 100 }).then(() => {
    // Make predictions
    const new_data = tf.tensor2d([[2, 3, 4, 200, 1, 1500]]); // Example input for prediction
    const predictions = model.predict(new_data);

    // Display predictions
    console.log('Predicted cluster_no:', Math.round(predictions.dataSync()[0]));
  });
}).catch((error) => {
  console.error('Error loading data:', error);
});
