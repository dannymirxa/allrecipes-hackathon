--
-- PostgreSQL database dump
--

\restrict qb0ioqCWkFcLrekMFx4aSb60zEGJ2tXNnUYfmjVLI4joZ2eIttQzE7hyep4hvR2

-- Dumped from database version 17.6 (Debian 17.6-1.pgdg13+1)
-- Dumped by pg_dump version 17.6 (Debian 17.6-1.pgdg13+1)

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
-- Name: categories; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.categories (
    recipe_id text,
    category text
);


ALTER TABLE public.categories OWNER TO myuser;

--
-- Name: ingredient_list; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ingredient_list (
    index bigint,
    id text,
    "ingredientId" text,
    "searchValue" text,
    term text,
    "useCount" bigint
);


ALTER TABLE public.ingredient_list OWNER TO myuser;

--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ingredients (
    recipe_id text,
    ingredient text
);


ALTER TABLE public.ingredients OWNER TO myuser;

--
-- Name: instructions; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.instructions (
    recipe_id text,
    step_number bigint,
    description text
);


ALTER TABLE public.instructions OWNER TO myuser;

--
-- Name: nutrition; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.nutrition (
    recipe_id text,
    calories text,
    servings text,
    total_fat text,
    saturated_fat text,
    cholesterol text,
    sodium text,
    potassium text,
    total_carbohydrate text,
    dietry_fibre text,
    protein text,
    sugars text,
    vitamin_a text,
    vitamin_c text,
    calcium text,
    iron text,
    thiamin text,
    niacin text,
    vitamin_b6 text,
    magnesium text,
    folate text
);


ALTER TABLE public.nutrition OWNER TO myuser;

--
-- Name: recipes; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.recipes (
    id text,
    title text,
    description text,
    prep_time text,
    cook_time text,
    total_time text,
    servings text,
    cuisine text,
    author text
);


ALTER TABLE public.recipes OWNER TO myuser;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.reviews (
    recipe_id text,
    user_name text
);


ALTER TABLE public.reviews OWNER TO myuser;

--
-- Name: ix_ingredient_list_index; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX ix_ingredient_list_index ON public.ingredient_list USING btree (index);


--
-- PostgreSQL database dump complete
--

\unrestrict qb0ioqCWkFcLrekMFx4aSb60zEGJ2tXNnUYfmjVLI4joZ2eIttQzE7hyep4hvR2

