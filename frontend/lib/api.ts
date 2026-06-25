import { useState } from 'react';

export type ApiResponse<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

export type ApiError = {
  message: string;
  code?: string;
};

export const useApi = <T,>() => {
  const [state, setState] = useState<ApiResponse<T>>({
    data: null,
    loading: false,
    error: null
  });

  const execute = async (promise: Promise<any>) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const result = await promise;
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (error: any) {
      const errorMessage = error.response?.data?.message ||
                          error.message ||
                          'An unknown error occurred';
      setState(prev => ({ ...prev, loading: false, error: errorMessage }));
      throw error;
    }
  };

  const reset = () => {
    setState({ data: null, loading: false, error: null });
  };

  return [state, { execute, reset }] as const;
};