# ResumeTailor Frontend

This is the frontend for the ResumeTailor application, built with [Next.js](https://nextjs.org) (App Router), TypeScript, and Tailwind CSS.

## Project Overview

ResumeTailor is an AI-powered web application that helps job seekers create optimized resumes tailored to specific job descriptions. Users upload their existing resume and provide a target job description, and the system generates a new, professional resume optimized for Applicant Tracking Systems (ATS).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Project Structure

- `app/`: Next.js app router pages and layouts
- `components/`: Reusable React components
- `lib/`: Utility functions and API clients
- `types/`: TypeScript type definitions
- `public/`: Static assets

## Features

- Resume upload (PDF/DOCX)
- Job description input
- AI-powered resume tailoring
- ATS-friendly PDF/DOCX generation
- One-click download
- Responsive design

## API Integration

The frontend communicates with the backend API at `/api/v1/` (proxy configured in `next.config.js` for development).

Key endpoints:
- `POST /api/v1/generate-optimized-resume`: Upload resume and job description to get optimized resume
- `GET /api/v1/download/{format}/{file_id}`: Download generated resume in PDF or DOCX format

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.