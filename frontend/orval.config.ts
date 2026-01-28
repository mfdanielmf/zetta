import { defineConfig } from 'orval';

export default defineConfig({
  zetta_backend: {
    output: {
      mode: 'split',
      target: 'src/api/backend.api.ts',
      schemas: 'src/api/model',
      client: 'vue-query',
      httpClient: 'axios',
      override: {
        mutator: {
          path: "src/api/axios.config.ts",
          name: "customInstance"
        }
      }
    },
    input: {
      target: 'http://localhost:8080/openapi.json',
    },
    hooks: {
      afterAllFilesWrite: 'prettier --write',
    },
  },
});
