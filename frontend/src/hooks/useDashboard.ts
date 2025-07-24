import { HealthCheckService } from "@/services/health_check";
import { useEffect } from "react";
import { useApi } from "./useApi";

export const useDashboard = () => {
  const { handleApiCall } = useApi();

  useEffect(() => {
    handleApiCall(HealthCheckService.check, () => {});
  }, []);

  return {};
};
