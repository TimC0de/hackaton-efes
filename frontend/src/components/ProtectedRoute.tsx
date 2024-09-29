import React from "react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
    isAuthenticated: boolean;
    children: JSX.Element;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ isAuthenticated, children }) => {
    if (!isAuthenticated) {
        // If user is not authenticated, redirect to login
        return <Navigate to="/login" />;
    }

    // If authenticated, render the protected component
    return children;
};

export default ProtectedRoute;
