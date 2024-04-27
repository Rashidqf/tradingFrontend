import React from 'react';
import './Loader.css';

export default function Loader() {
    return (
        <div className="min-h-screen w-full flex justify-center items-center">
            <div className="loader">
                <p className="heading">Loading</p>
                <div className="loading">
                    <div className="load"></div>
                    <div className="load"></div>
                    <div className="load"></div>
                    <div className="load"></div>
                </div>
            </div>
        </div>
    );
};
