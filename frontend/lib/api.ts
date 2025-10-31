/**
 * API Client for Movie Store Backend
 * 
 * This module provides functions to interact with the Flask backend API.
 * All requests go through Next.js rewrites (configured in next.config.ts)
 * which proxy to the backend service.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface Movie {
  id: number;
  title: string;
  director: string;
  year: string;
  genre: string[];
}

export interface MoviesResponse {
  movies: Movie[];
  _meta: {
    next: string | null;
    prev: string | null;
  };
}

export interface Category {
  id: number;
  genre: string;
  movies?: Movie[];
}

/**
 * Fetch all movies with pagination
 */
export async function fetchMovies(page = 1, perPage = 4): Promise<MoviesResponse> {
  const response = await fetch(
    `${API_BASE}/api/v1/movies?page=${page}&per_page=${perPage}`
  );
  
  if (!response.ok) {
    throw new Error(`Failed to fetch movies: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Search movies by genre
 */
export async function searchMoviesByGenre(genre: string, page = 1): Promise<MoviesResponse> {
  const response = await fetch(
    `${API_BASE}/api/v1/movies/search?genre=${encodeURIComponent(genre)}&page=${page}`
  );
  
  if (!response.ok) {
    throw new Error(`Failed to search movies: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Get a single movie by ID
 */
export async function fetchMovieById(id: number): Promise<Movie> {
  const response = await fetch(`${API_BASE}/api/v1/movies/${id}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch movie: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Fetch all categories
 */
export async function fetchCategories(): Promise<{ categories: Category[] }> {
  const response = await fetch(`${API_BASE}/api/v1/categories`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch categories: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Fetch categories with their movies
 */
export async function fetchCategoriesWithMovies(genre?: string): Promise<{ categories: Category[] }> {
  const url = genre 
    ? `${API_BASE}/api/v1/categories?genre=${encodeURIComponent(genre)}`
    : `${API_BASE}/api/v1/categories?genre=all`;
    
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch categories with movies: ${response.statusText}`);
  }
  
  return response.json();
}

