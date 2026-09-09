FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose port and start Vite dev server
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]

