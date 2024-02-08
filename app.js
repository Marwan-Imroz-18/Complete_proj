const express = require('express');
const app = express();
const { spawn } = require('child_process');

app.use(express.json());

app.post('/detect_differences', (req, res) => {
    // Extract the image paths from the request body
    const { image1_path, image2_path } = req.body;

    // Spawn a child process to run the Python script
    const process = spawn('python', ['app.py', image1_path, image2_path]);

    // Define variables to store response data
    let imageData = Buffer.alloc(0);
    let responseData = '';

    // Capture stdout data from the child process
    process.stdout.on('data', data => {
        if (Buffer.isBuffer(data)) {
            // Concatenate binary image data
            imageData = Buffer.concat([imageData, data]);
        } else {
            // Capture other response data
            responseData += data.toString();
        }
    });

    // Handle process close event
    process.on('close', code => {
        console.log(`child process close all stdio with code ${code}`);
        // Send the response
        res.json({
            imageData: imageData.toString('base64'), // Convert binary image data to base64
            responseData: responseData // Send other response data
        });
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});