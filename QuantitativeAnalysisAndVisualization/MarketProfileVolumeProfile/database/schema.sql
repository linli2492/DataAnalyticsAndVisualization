--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: datetime_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datetime_table (
    datetime_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL
);


ALTER TABLE public.datetime_table OWNER TO postgres;

--
-- Name: datetime_table_datetime_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datetime_table_datetime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datetime_table_datetime_id_seq OWNER TO postgres;

--
-- Name: datetime_table_datetime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datetime_table_datetime_id_seq OWNED BY public.datetime_table.datetime_id;


--
-- Name: futures_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.futures_table (
    futures_id integer NOT NULL,
    futures character varying(20) NOT NULL
);


ALTER TABLE public.futures_table OWNER TO postgres;

--
-- Name: futures_table_futures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.futures_table_futures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.futures_table_futures_id_seq OWNER TO postgres;

--
-- Name: futures_table_futures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.futures_table_futures_id_seq OWNED BY public.futures_table.futures_id;


--
-- Name: price_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_table (
    price_id integer NOT NULL,
    futures_id integer,
    datetime_id integer,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume integer
);


ALTER TABLE public.price_table OWNER TO postgres;

--
-- Name: price_table_price_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.price_table_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.price_table_price_id_seq OWNER TO postgres;

--
-- Name: price_table_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.price_table_price_id_seq OWNED BY public.price_table.price_id;


--
-- Name: datetime_table datetime_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datetime_table ALTER COLUMN datetime_id SET DEFAULT nextval('public.datetime_table_datetime_id_seq'::regclass);


--
-- Name: futures_table futures_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.futures_table ALTER COLUMN futures_id SET DEFAULT nextval('public.futures_table_futures_id_seq'::regclass);


--
-- Name: price_table price_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_table ALTER COLUMN price_id SET DEFAULT nextval('public.price_table_price_id_seq'::regclass);


--
-- Name: datetime_table datetime_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datetime_table
    ADD CONSTRAINT datetime_table_pkey PRIMARY KEY (datetime_id);


--
-- Name: futures_table futures_table_futures_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.futures_table
    ADD CONSTRAINT futures_table_futures_key UNIQUE (futures);


--
-- Name: futures_table futures_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.futures_table
    ADD CONSTRAINT futures_table_pkey PRIMARY KEY (futures_id);


--
-- Name: price_table price_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_table
    ADD CONSTRAINT price_table_pkey PRIMARY KEY (price_id);


--
-- Name: price_table price_table_datetime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_table
    ADD CONSTRAINT price_table_datetime_id_fkey FOREIGN KEY (datetime_id) REFERENCES public.datetime_table(datetime_id);


--
-- Name: price_table price_table_futures_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_table
    ADD CONSTRAINT price_table_futures_id_fkey FOREIGN KEY (futures_id) REFERENCES public.futures_table(futures_id);


--
-- PostgreSQL database dump complete
--

