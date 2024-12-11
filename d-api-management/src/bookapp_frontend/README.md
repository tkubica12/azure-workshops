# Frontend Application

This is the frontend application for managing books, reviews, and lists. It is built using React.

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Getting Started

1. Clone the repository:

   ```sh
   git clone https://github.com/tkubica12/jnt-apim-hackathon.git
   cd jnt-apim-hackathon/src/frontend
   ```

2. Install the dependencies:

   ```sh
   npm install
   ```

3. Start the development server:

   ```sh
   npm start
   ```

   The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build of the application, run:

```sh
npm run build
```

The production build will be available in the `build` directory.

## Docker

To build and run the application using Docker, follow these steps:

1. Build the Docker image:

   ```sh
   docker build -t frontend-app .
   ```

2. Run the Docker container:

   ```sh
   docker run -p 3000:3000 frontend-app
   ```

   The application will be available at `http://localhost:3000`.

## Project Structure

- `src/`: Contains the source code of the application.
  - `components/`: Contains the React components.
  - `pages/`: Contains the page components.
  - `services/`: Contains the services for API calls.
  - `App.js`: The main component of the application.
  - `index.js`: The entry point of the application.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a descriptive message.
4. Push your changes to your forked repository.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for more information.
