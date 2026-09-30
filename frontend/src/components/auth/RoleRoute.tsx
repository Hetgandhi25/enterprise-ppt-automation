import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../stores/useAuthStore";
import { toast } from "sonner";
import { useEffect } from "react";

interface Props {
  allowedRoles: string[];
}

export function RoleRoute({ allowedRoles }: Props) {
  const { user, token } = useAuthStore();

  useEffect(() => {
    if (token && user && !allowedRoles.includes(user.role)) {
      toast.error("Access Denied: You do not have permission to view this page.");
    }
  }, [user, token, allowedRoles]);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (!user || !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
