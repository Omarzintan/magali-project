function reportReading() {
    // Pick any temperature from a range of -5 to 15
    const temperature = (Math.random() * 20) - 5;
    // Write with newline char
    process.stdout.write(temperature + '\n');
    // Wait 0 to 5 seconds
    setTimeout(reportReading, Math.random() * 5000);
}
reportReading();
