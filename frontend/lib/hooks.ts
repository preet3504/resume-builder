import { useState } from 'react';

export const useFormState = <T extends Record<string, any>>(initialState: T) => {
  const [formState, setFormState] = useState<T>(() => ({ ...initialState }));

  const setField = <K extends keyof T>(key: K, value: T[K]) => {
    setFormState(prev => ({ ...prev, [key]: value }));
  };

  const reset = () => {
    setFormState(() => ({ ...initialState }));
  };

  return [formState, setField, reset] as const;
};

export const useApiState = <T>() => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const setDataState = (newData: T | null) => {
    setData(newData);
  };

  const setLoadingState = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  const setErrorState = (err: string | null) => {
    setError(err);
  };

  return [
    { data, loading, error },
    { setDataState, setLoadingState, setErrorState }
  ] as const;
};