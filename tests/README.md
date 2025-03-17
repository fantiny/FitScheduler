# API Testing Guide

This guide explains how to set up and run tests for the booking platform API.

## Requirements

- Python 3.8+
- pytest
- requests

## Installation

Install the required packages:

```bash
pip install pytest requests
```

## Test Setup

Before running the tests, it's recommended to populate the database with test data. This is necessary because many of the tests rely on existing data (venues, coaches, bookings, etc.) being available.

Run the test setup script to populate the database:

```bash
python test_setup.py
```

This script will:
1. Create a test user (or use existing one)
2. Create a test venue
3. Create a test coach
4. Create a test booking
5. Create a test review

## Running Tests

After setting up the test data, you can run all tests with:

```bash
pytest test.py -v
```

Or run specific test classes:

```bash
pytest test.py::TestVenues -v
pytest test.py::TestCoaches -v
pytest test.py::TestBookings -v
```

## Test Strategy

The tests follow these principles:

1. **Dynamic Testing**: Tests adapt to the existing data in the database rather than assuming specific IDs
2. **Skip When Needed**: Tests that require certain data will be skipped if that data doesn't exist
3. **Lenient Assertions**: Accept multiple status codes to accommodate different server behaviors
4. **Schema Compliance**: Request payloads are structured to match the expected API schemas

## Troubleshooting

If tests fail, check these common issues:

1. **Server Not Running**: Ensure the API server is running at `http://localhost:8000`
2. **Authentication Issues**: The test user must be able to register or login
3. **Schema Changes**: If the API schemas change, update the test payloads accordingly
4. **Missing Prerequisites**: Some tests require specific data to exist (e.g., lesson types)

## Test Results

Check the test report for a summary of test results:

```bash
pytest test.py -v --html=report.html
```

This will generate an HTML report with detailed test results. 