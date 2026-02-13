# Use Node image to build the app
FROM node:22

# Working dir in the container
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source
COPY . .

# Expose the port
EXPOSE 5173

# Run the server in dev mode
CMD ["npm", "run", "dev", "--", "--host"]
