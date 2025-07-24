import { useState } from "react";

export const useApi = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleApiCall = async <ReturnDataType>(
    apiCall: () => Promise<ReturnDataType>,
    onComplete?: () => void,
  ) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiCall();
      return response;
    } catch (err) {
      setError("An error occurred while fetching data");
      console.error(err);
      throw err; // Re-throw to handle in component
    } finally {
      setLoading(false);
      if (onComplete) onComplete();
    }
  };

  return {
    loading,
    error,
    handleApiCall,
  };
};
