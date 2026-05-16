-- ============================================
-- Deciora Database Schema for Supabase
-- Run this in your Supabase SQL Editor
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Users Table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.users (
    id            UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    company_name  TEXT,
    business_type TEXT,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ── Uploaded Files Table ───────────────────────────────────
CREATE TABLE IF NOT EXISTS public.uploaded_files (
    file_id      UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id      UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    session_id   UUID,
    file_name    TEXT NOT NULL,
    file_url     TEXT NOT NULL,
    file_size    BIGINT,
    file_type    TEXT,
    upload_date  TIMESTAMPTZ DEFAULT NOW()
);

-- ── Analysis Sessions Table ────────────────────────────────
CREATE TABLE IF NOT EXISTS public.analysis_sessions (
    session_id    UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id       UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    analysis_name TEXT NOT NULL DEFAULT 'New Analysis',
    analysis_type TEXT[],
    status        TEXT DEFAULT 'active',
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Add FK from uploaded_files to sessions
ALTER TABLE public.uploaded_files
    ADD CONSTRAINT fk_uploaded_files_session
    FOREIGN KEY (session_id)
    REFERENCES public.analysis_sessions(session_id)
    ON DELETE SET NULL;

-- ── Insights Table ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.insights (
    insight_id          UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id          UUID REFERENCES public.analysis_sessions(session_id)
                            ON DELETE CASCADE NOT NULL,
    generated_insights  JSONB,
    charts_data         JSONB,
    recommendations     JSONB,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ── Chat Messages Table ────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.chat_messages (
    message_id      UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id      UUID REFERENCES public.analysis_sessions(session_id)
                        ON DELETE CASCADE NOT NULL,
    sender_type     TEXT NOT NULL CHECK (sender_type IN ('user', 'assistant')),
    message_content TEXT NOT NULL,
    metadata        JSONB,
    timestamp       TIMESTAMPTZ DEFAULT NOW()
);

-- ── Feedback Table ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.feedback (
    feedback_id   UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id       UUID REFERENCES public.users(id) ON DELETE SET NULL,
    feedback_type TEXT CHECK (
                    feedback_type IN (
                        'suggestion','bug',
                        'feature_request','general'
                    )),
    message       TEXT NOT NULL,
    email         TEXT,
    timestamp     TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- Row Level Security
-- ============================================

ALTER TABLE public.users           ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uploaded_files  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analysis_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.insights        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback        ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users view own profile"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users update own profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Users insert own profile"
    ON public.users FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Uploaded files policies
CREATE POLICY "Users manage own files"
    ON public.uploaded_files FOR ALL
    USING (auth.uid() = user_id);

-- Sessions policies
CREATE POLICY "Users manage own sessions"
    ON public.analysis_sessions FOR ALL
    USING (auth.uid() = user_id);

-- Insights policies
CREATE POLICY "Users view own insights"
    ON public.insights FOR ALL
    USING (
        session_id IN (
            SELECT session_id
            FROM public.analysis_sessions
            WHERE user_id = auth.uid()
        )
    );

-- Chat messages policies
CREATE POLICY "Users view own messages"
    ON public.chat_messages FOR ALL
    USING (
        session_id IN (
            SELECT session_id
            FROM public.analysis_sessions
            WHERE user_id = auth.uid()
        )
    );

-- Feedback policies
CREATE POLICY "Anyone can submit feedback"
    ON public.feedback FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users view own feedback"
    ON public.feedback FOR SELECT
    USING (auth.uid() = user_id OR user_id IS NULL);

-- ============================================
-- Auto Create User Profile on Signup
-- ============================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email)
    VALUES (NEW.id, NEW.email)
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- Performance Indexes
-- ============================================

CREATE INDEX IF NOT EXISTS idx_sessions_user
    ON public.analysis_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_sessions_updated
    ON public.analysis_sessions(updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_files_session
    ON public.uploaded_files(session_id);

CREATE INDEX IF NOT EXISTS idx_messages_session
    ON public.chat_messages(session_id);

CREATE INDEX IF NOT EXISTS idx_messages_timestamp
    ON public.chat_messages(timestamp ASC);

CREATE INDEX IF NOT EXISTS idx_insights_session
    ON public.insights(session_id);

-- ============================================
-- Storage Bucket
-- Run separately in Supabase Storage tab:
-- Create bucket named: deciora-files
-- Set to: Private
-- ============================================