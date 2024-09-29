import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import DashboardPage from "./DashboardPage";
import LoginPage from "./LoginPage.tsx";
import ProtectedRoute from "./ProtectedRoute";
import ViewPage from "./ViewPage";

import axios from "axios";

export const axiosPublic = axios.create({
    baseURL: import.meta.env.VITE_SERVER_URL,
    headers: {
        "Content-Type": "multipart/form-data",
    },
});

const AppRouter: React.FC = () => {
    // Simulate logged-in state
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

    const login = () => {
        setIsAuthenticated(true);
    };

    const logout = () => {
        setIsAuthenticated(false);
    };

    return (
        <Router>
            <Routes>
                {/* Login route */}
                <Route path="/login" element={<LoginPage login={login} />} />

                {/* Public route (home) */}
                <Route path="/" element={<Navigate to="/dashboard" />} />

                {/* Redirect unknown paths to login */}
                <Route path="*" element={<Navigate to="/dashboard" />} />

                {/* Protected routes */}
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <DashboardPage logout={logout} />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/view/:id"
                    element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <ViewPage />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
};

export default AppRouter;
