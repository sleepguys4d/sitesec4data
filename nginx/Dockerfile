# Etapa 1 — build do Back Office (React/Vite)
FROM node:20-alpine AS admin-build
WORKDIR /admin
COPY admin/package*.json ./
RUN npm install
COPY admin/ .
RUN npm run build

# Etapa 2 — imagem final nginx, a servir o site + o back office + proxy da API
FROM nginx:1.27-alpine
COPY site/ /usr/share/nginx/html/
COPY --from=admin-build /admin/dist /usr/share/nginx/html/admin
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
