import Axios from 'axios';
import type { AxiosRequestConfig } from 'axios';

export const AXIOS_INSTANCE = Axios.create({
  baseURL: 'http://localhost:8080'
});

export const customInstance = <T>(
  config: AxiosRequestConfig,
  options?: AxiosRequestConfig,
): Promise<T> => {
  const promise = AXIOS_INSTANCE({
    ...config,
    ...options,
  }).then(({ data }) => data);

  return promise;
};

export type BodyType<BodyData> = BodyData;
