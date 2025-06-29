PGDMP      4                }            task_manager    17.4    17.4 �    	           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    16388    task_manager    DATABASE     r   CREATE DATABASE task_manager WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE task_manager;
                     postgres    false                        2615    17882    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                     postgres    false                       0    0    SCHEMA public    COMMENT         COMMENT ON SCHEMA public IS '';
                        postgres    false    5                       0    0    SCHEMA public    ACL     +   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
                        postgres    false    5            }           1247    17884    cassettetypeenum    TYPE     ~   CREATE TYPE public.cassettetypeenum AS ENUM (
    'KZT_STD',
    'KOT_STD',
    'KOTVO',
    'KZT',
    'KOT',
    'OTHER'
);
 #   DROP TYPE public.cassettetypeenum;
       public               postgres    false    5            �           1247    17898    klamertypeenum    TYPE     \   CREATE TYPE public.klamertypeenum AS ENUM (
    'IN_LINE',
    'STARTING',
    'ANGULAR'
);
 !   DROP TYPE public.klamertypeenum;
       public               postgres    false    5            �           1247    17906    managerenum    TYPE     �   CREATE TYPE public.managerenum AS ENUM (
    'NOVIKOV',
    'SEMICHEV',
    'PTICHKINA',
    'VIKULINA',
    'GAVRILOVEC',
    'SEMICHEV_YOUNGER'
);
    DROP TYPE public.managerenum;
       public               postgres    false    5            �           1247    17920    materialthicknessenum    TYPE     �   CREATE TYPE public.materialthicknessenum AS ENUM (
    'ZERO_FIVE',
    'ZERO_SEVEN',
    'ONE',
    'ONE_TWO',
    'ONE_FIVE',
    'TWO',
    'THREE'
);
 (   DROP TYPE public.materialthicknessenum;
       public               postgres    false    5            �           1247    17936    materialtypeenum    TYPE     �   CREATE TYPE public.materialtypeenum AS ENUM (
    'ALUMINIUM',
    'STEEL',
    'STAINLESS_STEEL',
    'ZINC',
    'POLYMER'
);
 #   DROP TYPE public.materialtypeenum;
       public               postgres    false    5            �           1247    17948    producttypeenum    TYPE     �   CREATE TYPE public.producttypeenum AS ENUM (
    'PROFILE',
    'KLAMER',
    'BRACKET',
    'EXTENSION_BRACKET',
    'CASSETTE',
    'FACING',
    'LINEAR_PANEL',
    'SHEET',
    'WALL_PANEL'
);
 "   DROP TYPE public.producttypeenum;
       public               postgres    false    5            �           1247    17968    profiletypeenum    TYPE     �   CREATE TYPE public.profiletypeenum AS ENUM (
    'G40X40',
    'G40X60',
    'G50X50',
    'P60',
    'P80',
    'P100',
    'Z20X20X40',
    'PGSH',
    'PVSH',
    'PNU'
);
 "   DROP TYPE public.profiletypeenum;
       public               postgres    false    5            �           1247    17990 
   statusenum    TYPE     t   CREATE TYPE public.statusenum AS ENUM (
    'NEW',
    'IN_WORK',
    'COMPLETED',
    'CANCELED',
    'ON_HOLD'
);
    DROP TYPE public.statusenum;
       public               postgres    false    5            �           1247    18002    urgencyenum    TYPE     P   CREATE TYPE public.urgencyenum AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH'
);
    DROP TYPE public.urgencyenum;
       public               postgres    false    5            �           1247    18010    usertypeenum    TYPE     k   CREATE TYPE public.usertypeenum AS ENUM (
    'ADMIN',
    'ENGINEER',
    'OPERATOR',
    'SUPERVISER'
);
    DROP TYPE public.usertypeenum;
       public               postgres    false    5            �           1247    18020    workshopenum    TYPE     �   CREATE TYPE public.workshopenum AS ENUM (
    'PROFILE',
    'KLAMER',
    'BRACKET',
    'EXTENSION_BRACKET',
    'ENGINEER',
    'BENDING',
    'CUTTING',
    'COORDINATE_PUNCHING',
    'PAINTING'
);
    DROP TYPE public.workshopenum;
       public               postgres    false    5            �            1259    18039    bid    TABLE     �   CREATE TABLE public.bid (
    id integer NOT NULL,
    task_number integer,
    customer_id integer NOT NULL,
    manager public.managerenum NOT NULL,
    status public.statusenum DEFAULT 'NEW'::public.statusenum
);
    DROP TABLE public.bid;
       public         heap r       postgres    false    914    899    5    914            �            1259    18043 
   bid_id_seq    SEQUENCE     �   CREATE SEQUENCE public.bid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.bid_id_seq;
       public               postgres    false    217    5                       0    0 
   bid_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.bid_id_seq OWNED BY public.bid.id;
          public               postgres    false    218            �            1259    18044    bracket    TABLE     �   CREATE TABLE public.bracket (
    id integer NOT NULL,
    product_id integer NOT NULL,
    width integer NOT NULL,
    length character varying NOT NULL
);
    DROP TABLE public.bracket;
       public         heap r       postgres    false    5            �            1259    18049    bracket_id_seq    SEQUENCE     �   CREATE SEQUENCE public.bracket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.bracket_id_seq;
       public               postgres    false    219    5                       0    0    bracket_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.bracket_id_seq OWNED BY public.bracket.id;
          public               postgres    false    220            �            1259    18050    cassette    TABLE     �   CREATE TABLE public.cassette (
    id integer NOT NULL,
    product_id integer NOT NULL,
    cassette_type public.cassettetypeenum NOT NULL
);
    DROP TABLE public.cassette;
       public         heap r       postgres    false    893    5            �            1259    18053    cassette_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cassette_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.cassette_id_seq;
       public               postgres    false    221    5                       0    0    cassette_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.cassette_id_seq OWNED BY public.cassette.id;
          public               postgres    false    222                       1259    18357    clamp_locations    TABLE     �   CREATE TABLE public.clamp_locations (
    id integer NOT NULL,
    nest_file_id integer NOT NULL,
    clamp_1 integer NOT NULL,
    clamp_2 integer NOT NULL,
    clamp_3 integer NOT NULL
);
 #   DROP TABLE public.clamp_locations;
       public         heap r       postgres    false    5                       1259    18356    clamp_locations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.clamp_locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.clamp_locations_id_seq;
       public               postgres    false    260    5                       0    0    clamp_locations_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.clamp_locations_id_seq OWNED BY public.clamp_locations.id;
          public               postgres    false    259            �            1259    18054    comment    TABLE     �   CREATE TABLE public.comment (
    id integer NOT NULL,
    user_id integer NOT NULL,
    content character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    is_read boolean NOT NULL,
    bid_id integer
);
    DROP TABLE public.comment;
       public         heap r       postgres    false    5            �            1259    18058    comment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.comment_id_seq;
       public               postgres    false    223    5                       0    0    comment_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;
          public               postgres    false    224            �            1259    18059    customer    TABLE     c   CREATE TABLE public.customer (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.customer;
       public         heap r       postgres    false    5            �            1259    18062    customer_id_seq    SEQUENCE     �   CREATE SEQUENCE public.customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.customer_id_seq;
       public               postgres    false    225    5                       0    0    customer_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.id;
          public               postgres    false    226            �            1259    18063    extension_bracket    TABLE     �   CREATE TABLE public.extension_bracket (
    id integer NOT NULL,
    product_id integer NOT NULL,
    width integer NOT NULL,
    length character varying NOT NULL,
    heel boolean NOT NULL
);
 %   DROP TABLE public.extension_bracket;
       public         heap r       postgres    false    5            �            1259    18068    extension_bracket_id_seq    SEQUENCE     �   CREATE SEQUENCE public.extension_bracket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.extension_bracket_id_seq;
       public               postgres    false    227    5                       0    0    extension_bracket_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.extension_bracket_id_seq OWNED BY public.extension_bracket.id;
          public               postgres    false    228            �            1259    18069    files    TABLE     �   CREATE TABLE public.files (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    filename character varying(255) NOT NULL,
    file_type character varying NOT NULL,
    file_path character varying(255) NOT NULL
);
    DROP TABLE public.files;
       public         heap r       postgres    false    5            �            1259    18074    files_id_seq    SEQUENCE     �   CREATE SEQUENCE public.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.files_id_seq;
       public               postgres    false    5    229                       0    0    files_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;
          public               postgres    false    230            �            1259    18075    klamer    TABLE     �   CREATE TABLE public.klamer (
    id integer NOT NULL,
    product_id integer NOT NULL,
    klamer_type public.klamertypeenum NOT NULL
);
    DROP TABLE public.klamer;
       public         heap r       postgres    false    896    5            �            1259    18078    klamer_id_seq    SEQUENCE     �   CREATE SEQUENCE public.klamer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.klamer_id_seq;
       public               postgres    false    5    231                       0    0    klamer_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.klamer_id_seq OWNED BY public.klamer.id;
          public               postgres    false    232            �            1259    18079    linear_panel    TABLE     �   CREATE TABLE public.linear_panel (
    id integer NOT NULL,
    product_id integer NOT NULL,
    field integer NOT NULL,
    rust integer NOT NULL,
    length integer NOT NULL,
    butt_end boolean NOT NULL
);
     DROP TABLE public.linear_panel;
       public         heap r       postgres    false    5            �            1259    18082    linear_panel_id_seq    SEQUENCE     �   CREATE SEQUENCE public.linear_panel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.linear_panel_id_seq;
       public               postgres    false    5    233                       0    0    linear_panel_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.linear_panel_id_seq OWNED BY public.linear_panel.id;
          public               postgres    false    234            �            1259    18083    material    TABLE     �   CREATE TABLE public.material (
    id integer NOT NULL,
    type public.materialtypeenum NOT NULL,
    thickness public.materialthicknessenum NOT NULL,
    color character varying(50),
    waste double precision
);
    DROP TABLE public.material;
       public         heap r       postgres    false    905    902    5            �            1259    18086    material_id_seq    SEQUENCE     �   CREATE SEQUENCE public.material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.material_id_seq;
       public               postgres    false    5    235                       0    0    material_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.material_id_seq OWNED BY public.material.id;
          public               postgres    false    236                       1259    18343 	   nest_file    TABLE       CREATE TABLE public.nest_file (
    id integer NOT NULL,
    file_id integer NOT NULL,
    nest_id integer NOT NULL,
    material character varying(50) NOT NULL,
    thickness character varying(50) NOT NULL,
    nc_file_name character varying(50) NOT NULL,
    sheet_size character varying(50) NOT NULL,
    time_per_sheet character varying(50) NOT NULL,
    nest_notes character varying(255),
    sheet_quantity integer NOT NULL,
    nest_screen_file_path character varying(255) NOT NULL,
    sheet_utilization double precision NOT NULL
);
    DROP TABLE public.nest_file;
       public         heap r       postgres    false    5                       1259    18342    nest_file_id_seq    SEQUENCE     �   CREATE SEQUENCE public.nest_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.nest_file_id_seq;
       public               postgres    false    258    5                       0    0    nest_file_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.nest_file_id_seq OWNED BY public.nest_file.id;
          public               postgres    false    257                       1259    18371    parts    TABLE     �   CREATE TABLE public.parts (
    id integer NOT NULL,
    nest_file_id integer NOT NULL,
    part_id integer NOT NULL,
    name character varying(50) NOT NULL,
    quantity integer NOT NULL,
    time_per_part character varying(50) NOT NULL
);
    DROP TABLE public.parts;
       public         heap r       postgres    false    5                       1259    18370    parts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.parts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.parts_id_seq;
       public               postgres    false    262    5                       0    0    parts_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.parts_id_seq OWNED BY public.parts.id;
          public               postgres    false    261            �            1259    18087    product    TABLE     c   CREATE TABLE public.product (
    id integer NOT NULL,
    type public.producttypeenum NOT NULL
);
    DROP TABLE public.product;
       public         heap r       postgres    false    908    5            �            1259    18090    product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.product_id_seq;
       public               postgres    false    237    5                       0    0    product_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;
          public               postgres    false    238            �            1259    18091    profile    TABLE     �   CREATE TABLE public.profile (
    id integer NOT NULL,
    product_id integer NOT NULL,
    profile_type public.profiletypeenum NOT NULL,
    length integer NOT NULL
);
    DROP TABLE public.profile;
       public         heap r       postgres    false    5    911            �            1259    18094    profile_id_seq    SEQUENCE     �   CREATE SEQUENCE public.profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.profile_id_seq;
       public               postgres    false    5    239                       0    0    profile_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.profile_id_seq OWNED BY public.profile.id;
          public               postgres    false    240            �            1259    18095    sheets    TABLE     �   CREATE TABLE public.sheets (
    id integer NOT NULL,
    task_id integer NOT NULL,
    width integer NOT NULL,
    length integer NOT NULL,
    quantity integer NOT NULL
);
    DROP TABLE public.sheets;
       public         heap r       postgres    false    5            �            1259    18098    sheets_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sheets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.sheets_id_seq;
       public               postgres    false    241    5                       0    0    sheets_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.sheets_id_seq OWNED BY public.sheets.id;
          public               postgres    false    242            �            1259    18099    task    TABLE     Q  CREATE TABLE public.task (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    material_id integer NOT NULL,
    urgency public.urgencyenum NOT NULL,
    status public.statusenum DEFAULT 'NEW'::public.statusenum NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    completed_at timestamp with time zone
);
    DROP TABLE public.task;
       public         heap r       postgres    false    914    5    914    917            �            1259    18104    task_id_seq    SEQUENCE     �   CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.task_id_seq;
       public               postgres    false    243    5                       0    0    task_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;
          public               postgres    false    244            �            1259    18105    task_products    TABLE       CREATE TABLE public.task_products (
    id integer NOT NULL,
    task_id integer NOT NULL,
    product_id integer NOT NULL,
    color character varying,
    quantity integer NOT NULL,
    done_quantity integer NOT NULL,
    painting boolean DEFAULT false,
    description text
);
 !   DROP TABLE public.task_products;
       public         heap r       postgres    false    5            �            1259    18111    task_products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.task_products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.task_products_id_seq;
       public               postgres    false    245    5                        0    0    task_products_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.task_products_id_seq OWNED BY public.task_products.id;
          public               postgres    false    246            �            1259    18112    task_responsible_association    TABLE     q   CREATE TABLE public.task_responsible_association (
    task_id integer NOT NULL,
    user_id integer NOT NULL
);
 0   DROP TABLE public.task_responsible_association;
       public         heap r       postgres    false    5            �            1259    18115    task_workshops    TABLE     �   CREATE TABLE public.task_workshops (
    id integer NOT NULL,
    task_id integer NOT NULL,
    workshop_id integer NOT NULL,
    status public.statusenum NOT NULL,
    progress_percent double precision DEFAULT 0.0
);
 "   DROP TABLE public.task_workshops;
       public         heap r       postgres    false    5    914            �            1259    18119    task_workshops_id_seq    SEQUENCE     �   CREATE SEQUENCE public.task_workshops_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.task_workshops_id_seq;
       public               postgres    false    5    248            !           0    0    task_workshops_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.task_workshops_id_seq OWNED BY public.task_workshops.id;
          public               postgres    false    249                       1259    18383    tools    TABLE     2  CREATE TABLE public.tools (
    id integer NOT NULL,
    nest_file_id integer NOT NULL,
    station character varying(50) NOT NULL,
    tool character varying(50) NOT NULL,
    size character varying(50) NOT NULL,
    angle integer NOT NULL,
    hits integer NOT NULL,
    die double precision NOT NULL
);
    DROP TABLE public.tools;
       public         heap r       postgres    false    5                       1259    18382    tools_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tools_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.tools_id_seq;
       public               postgres    false    264    5            "           0    0    tools_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.tools_id_seq OWNED BY public.tools.id;
          public               postgres    false    263            �            1259    18120    user_workshop_association    TABLE     r   CREATE TABLE public.user_workshop_association (
    user_id integer NOT NULL,
    workshop_id integer NOT NULL
);
 -   DROP TABLE public.user_workshop_association;
       public         heap r       postgres    false    5            �            1259    18123    users    TABLE     z  CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    firstname character varying(50) NOT NULL,
    email character varying(100),
    telegram character varying(50),
    username character varying(50) NOT NULL,
    password character varying(60) NOT NULL,
    user_type public.usertypeenum NOT NULL,
    is_active boolean NOT NULL
);
    DROP TABLE public.users;
       public         heap r       postgres    false    920    5            �            1259    18126    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    5    251            #           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               postgres    false    252            �            1259    18127    weight    TABLE     �   CREATE TABLE public.weight (
    id integer NOT NULL,
    weight double precision NOT NULL,
    from_waste boolean DEFAULT false,
    material_id integer NOT NULL
);
    DROP TABLE public.weight;
       public         heap r       postgres    false    5            �            1259    18131    weight_id_seq    SEQUENCE     �   CREATE SEQUENCE public.weight_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.weight_id_seq;
       public               postgres    false    5    253            $           0    0    weight_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.weight_id_seq OWNED BY public.weight.id;
          public               postgres    false    254            �            1259    18132    workshop    TABLE     a   CREATE TABLE public.workshop (
    id integer NOT NULL,
    name public.workshopenum NOT NULL
);
    DROP TABLE public.workshop;
       public         heap r       postgres    false    923    5                        1259    18135    workshop_id_seq    SEQUENCE     �   CREATE SEQUENCE public.workshop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.workshop_id_seq;
       public               postgres    false    255    5            %           0    0    workshop_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.workshop_id_seq OWNED BY public.workshop.id;
          public               postgres    false    256            �           2604    18136    bid id    DEFAULT     `   ALTER TABLE ONLY public.bid ALTER COLUMN id SET DEFAULT nextval('public.bid_id_seq'::regclass);
 5   ALTER TABLE public.bid ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217            �           2604    18137 
   bracket id    DEFAULT     h   ALTER TABLE ONLY public.bracket ALTER COLUMN id SET DEFAULT nextval('public.bracket_id_seq'::regclass);
 9   ALTER TABLE public.bracket ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219            �           2604    18138    cassette id    DEFAULT     j   ALTER TABLE ONLY public.cassette ALTER COLUMN id SET DEFAULT nextval('public.cassette_id_seq'::regclass);
 :   ALTER TABLE public.cassette ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    221            �           2604    18360    clamp_locations id    DEFAULT     x   ALTER TABLE ONLY public.clamp_locations ALTER COLUMN id SET DEFAULT nextval('public.clamp_locations_id_seq'::regclass);
 A   ALTER TABLE public.clamp_locations ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    260    259    260            �           2604    18139 
   comment id    DEFAULT     h   ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);
 9   ALTER TABLE public.comment ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223            �           2604    18140    customer id    DEFAULT     j   ALTER TABLE ONLY public.customer ALTER COLUMN id SET DEFAULT nextval('public.customer_id_seq'::regclass);
 :   ALTER TABLE public.customer ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225            �           2604    18141    extension_bracket id    DEFAULT     |   ALTER TABLE ONLY public.extension_bracket ALTER COLUMN id SET DEFAULT nextval('public.extension_bracket_id_seq'::regclass);
 C   ALTER TABLE public.extension_bracket ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    227            �           2604    18142    files id    DEFAULT     d   ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);
 7   ALTER TABLE public.files ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    230    229            �           2604    18143 	   klamer id    DEFAULT     f   ALTER TABLE ONLY public.klamer ALTER COLUMN id SET DEFAULT nextval('public.klamer_id_seq'::regclass);
 8   ALTER TABLE public.klamer ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    232    231            �           2604    18144    linear_panel id    DEFAULT     r   ALTER TABLE ONLY public.linear_panel ALTER COLUMN id SET DEFAULT nextval('public.linear_panel_id_seq'::regclass);
 >   ALTER TABLE public.linear_panel ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    234    233            �           2604    18145    material id    DEFAULT     j   ALTER TABLE ONLY public.material ALTER COLUMN id SET DEFAULT nextval('public.material_id_seq'::regclass);
 :   ALTER TABLE public.material ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    236    235            �           2604    18346    nest_file id    DEFAULT     l   ALTER TABLE ONLY public.nest_file ALTER COLUMN id SET DEFAULT nextval('public.nest_file_id_seq'::regclass);
 ;   ALTER TABLE public.nest_file ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    258    257    258            �           2604    18374    parts id    DEFAULT     d   ALTER TABLE ONLY public.parts ALTER COLUMN id SET DEFAULT nextval('public.parts_id_seq'::regclass);
 7   ALTER TABLE public.parts ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    261    262    262            �           2604    18146 
   product id    DEFAULT     h   ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);
 9   ALTER TABLE public.product ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    238    237            �           2604    18147 
   profile id    DEFAULT     h   ALTER TABLE ONLY public.profile ALTER COLUMN id SET DEFAULT nextval('public.profile_id_seq'::regclass);
 9   ALTER TABLE public.profile ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    240    239            �           2604    18148 	   sheets id    DEFAULT     f   ALTER TABLE ONLY public.sheets ALTER COLUMN id SET DEFAULT nextval('public.sheets_id_seq'::regclass);
 8   ALTER TABLE public.sheets ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    242    241            �           2604    18149    task id    DEFAULT     b   ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);
 6   ALTER TABLE public.task ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    244    243            �           2604    18150    task_products id    DEFAULT     t   ALTER TABLE ONLY public.task_products ALTER COLUMN id SET DEFAULT nextval('public.task_products_id_seq'::regclass);
 ?   ALTER TABLE public.task_products ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    246    245            �           2604    18151    task_workshops id    DEFAULT     v   ALTER TABLE ONLY public.task_workshops ALTER COLUMN id SET DEFAULT nextval('public.task_workshops_id_seq'::regclass);
 @   ALTER TABLE public.task_workshops ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    249    248            �           2604    18386    tools id    DEFAULT     d   ALTER TABLE ONLY public.tools ALTER COLUMN id SET DEFAULT nextval('public.tools_id_seq'::regclass);
 7   ALTER TABLE public.tools ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    263    264    264            �           2604    18152    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    252    251            �           2604    18153 	   weight id    DEFAULT     f   ALTER TABLE ONLY public.weight ALTER COLUMN id SET DEFAULT nextval('public.weight_id_seq'::regclass);
 8   ALTER TABLE public.weight ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    254    253            �           2604    18154    workshop id    DEFAULT     j   ALTER TABLE ONLY public.workshop ALTER COLUMN id SET DEFAULT nextval('public.workshop_id_seq'::regclass);
 :   ALTER TABLE public.workshop ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    256    255            �          0    18039    bid 
   TABLE DATA           L   COPY public.bid (id, task_number, customer_id, manager, status) FROM stdin;
    public               postgres    false    217   �      �          0    18044    bracket 
   TABLE DATA           @   COPY public.bracket (id, product_id, width, length) FROM stdin;
    public               postgres    false    219   �      �          0    18050    cassette 
   TABLE DATA           A   COPY public.cassette (id, product_id, cassette_type) FROM stdin;
    public               postgres    false    221   '                0    18357    clamp_locations 
   TABLE DATA           V   COPY public.clamp_locations (id, nest_file_id, clamp_1, clamp_2, clamp_3) FROM stdin;
    public               postgres    false    260   M      �          0    18054    comment 
   TABLE DATA           T   COPY public.comment (id, user_id, content, created_at, is_read, bid_id) FROM stdin;
    public               postgres    false    223   j      �          0    18059    customer 
   TABLE DATA           ,   COPY public.customer (id, name) FROM stdin;
    public               postgres    false    225   �      �          0    18063    extension_bracket 
   TABLE DATA           P   COPY public.extension_bracket (id, product_id, width, length, heel) FROM stdin;
    public               postgres    false    227   �      �          0    18069    files 
   TABLE DATA           K   COPY public.files (id, bid_id, filename, file_type, file_path) FROM stdin;
    public               postgres    false    229         �          0    18075    klamer 
   TABLE DATA           =   COPY public.klamer (id, product_id, klamer_type) FROM stdin;
    public               postgres    false    231   n      �          0    18079    linear_panel 
   TABLE DATA           U   COPY public.linear_panel (id, product_id, field, rust, length, butt_end) FROM stdin;
    public               postgres    false    233   �      �          0    18083    material 
   TABLE DATA           E   COPY public.material (id, type, thickness, color, waste) FROM stdin;
    public               postgres    false    235   �                 0    18343 	   nest_file 
   TABLE DATA           �   COPY public.nest_file (id, file_id, nest_id, material, thickness, nc_file_name, sheet_size, time_per_sheet, nest_notes, sheet_quantity, nest_screen_file_path, sheet_utilization) FROM stdin;
    public               postgres    false    258   �                0    18371    parts 
   TABLE DATA           Y   COPY public.parts (id, nest_file_id, part_id, name, quantity, time_per_part) FROM stdin;
    public               postgres    false    262   �      �          0    18087    product 
   TABLE DATA           +   COPY public.product (id, type) FROM stdin;
    public               postgres    false    237          �          0    18091    profile 
   TABLE DATA           G   COPY public.profile (id, product_id, profile_type, length) FROM stdin;
    public               postgres    false    239   N       �          0    18095    sheets 
   TABLE DATA           F   COPY public.sheets (id, task_id, width, length, quantity) FROM stdin;
    public               postgres    false    241   }       �          0    18099    task 
   TABLE DATA           b   COPY public.task (id, bid_id, material_id, urgency, status, created_at, completed_at) FROM stdin;
    public               postgres    false    243   �       �          0    18105    task_products 
   TABLE DATA           w   COPY public.task_products (id, task_id, product_id, color, quantity, done_quantity, painting, description) FROM stdin;
    public               postgres    false    245   �       �          0    18112    task_responsible_association 
   TABLE DATA           H   COPY public.task_responsible_association (task_id, user_id) FROM stdin;
    public               postgres    false    247   "!      �          0    18115    task_workshops 
   TABLE DATA           \   COPY public.task_workshops (id, task_id, workshop_id, status, progress_percent) FROM stdin;
    public               postgres    false    248   ?!                0    18383    tools 
   TABLE DATA           X   COPY public.tools (id, nest_file_id, station, tool, size, angle, hits, die) FROM stdin;
    public               postgres    false    264   �!      �          0    18120    user_workshop_association 
   TABLE DATA           I   COPY public.user_workshop_association (user_id, workshop_id) FROM stdin;
    public               postgres    false    250   �!      �          0    18123    users 
   TABLE DATA           o   COPY public.users (id, name, firstname, email, telegram, username, password, user_type, is_active) FROM stdin;
    public               postgres    false    251   �!      �          0    18127    weight 
   TABLE DATA           E   COPY public.weight (id, weight, from_waste, material_id) FROM stdin;
    public               postgres    false    253   {#      �          0    18132    workshop 
   TABLE DATA           ,   COPY public.workshop (id, name) FROM stdin;
    public               postgres    false    255   �#      &           0    0 
   bid_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.bid_id_seq', 53, true);
          public               postgres    false    218            '           0    0    bracket_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.bracket_id_seq', 4, true);
          public               postgres    false    220            (           0    0    cassette_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.cassette_id_seq', 11, true);
          public               postgres    false    222            )           0    0    clamp_locations_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.clamp_locations_id_seq', 294, true);
          public               postgres    false    259            *           0    0    comment_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.comment_id_seq', 19, true);
          public               postgres    false    224            +           0    0    customer_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.customer_id_seq', 6, true);
          public               postgres    false    226            ,           0    0    extension_bracket_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.extension_bracket_id_seq', 2, true);
          public               postgres    false    228            -           0    0    files_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.files_id_seq', 444, true);
          public               postgres    false    230            .           0    0    klamer_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.klamer_id_seq', 4, true);
          public               postgres    false    232            /           0    0    linear_panel_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.linear_panel_id_seq', 1, true);
          public               postgres    false    234            0           0    0    material_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.material_id_seq', 48, true);
          public               postgres    false    236            1           0    0    nest_file_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.nest_file_id_seq', 299, true);
          public               postgres    false    257            2           0    0    parts_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.parts_id_seq', 741, true);
          public               postgres    false    261            3           0    0    product_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.product_id_seq', 64, true);
          public               postgres    false    238            4           0    0    profile_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.profile_id_seq', 17, true);
          public               postgres    false    240            5           0    0    sheets_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.sheets_id_seq', 13, true);
          public               postgres    false    242            6           0    0    task_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.task_id_seq', 44, true);
          public               postgres    false    244            7           0    0    task_products_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.task_products_id_seq', 21, true);
          public               postgres    false    246            8           0    0    task_workshops_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.task_workshops_id_seq', 85, true);
          public               postgres    false    249            9           0    0    tools_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.tools_id_seq', 1822, true);
          public               postgres    false    263            :           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 12, true);
          public               postgres    false    252            ;           0    0    weight_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.weight_id_seq', 3, true);
          public               postgres    false    254            <           0    0    workshop_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.workshop_id_seq', 18, true);
          public               postgres    false    256            �           2606    18156    bid bid_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.bid
    ADD CONSTRAINT bid_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.bid DROP CONSTRAINT bid_pkey;
       public                 postgres    false    217            �           2606    18158    bracket bracket_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.bracket
    ADD CONSTRAINT bracket_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.bracket DROP CONSTRAINT bracket_pkey;
       public                 postgres    false    219            �           2606    18160    cassette cassette_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.cassette
    ADD CONSTRAINT cassette_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.cassette DROP CONSTRAINT cassette_pkey;
       public                 postgres    false    221            %           2606    18364 0   clamp_locations clamp_locations_nest_file_id_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.clamp_locations
    ADD CONSTRAINT clamp_locations_nest_file_id_key UNIQUE (nest_file_id);
 Z   ALTER TABLE ONLY public.clamp_locations DROP CONSTRAINT clamp_locations_nest_file_id_key;
       public                 postgres    false    260            '           2606    18362 $   clamp_locations clamp_locations_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.clamp_locations
    ADD CONSTRAINT clamp_locations_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.clamp_locations DROP CONSTRAINT clamp_locations_pkey;
       public                 postgres    false    260            �           2606    18162    comment comment_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.comment DROP CONSTRAINT comment_pkey;
       public                 postgres    false    223            �           2606    18164    customer customer_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.customer DROP CONSTRAINT customer_name_key;
       public                 postgres    false    225            �           2606    18166    customer customer_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.customer DROP CONSTRAINT customer_pkey;
       public                 postgres    false    225            �           2606    18168 (   extension_bracket extension_bracket_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.extension_bracket
    ADD CONSTRAINT extension_bracket_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.extension_bracket DROP CONSTRAINT extension_bracket_pkey;
       public                 postgres    false    227            �           2606    18170    files files_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.files DROP CONSTRAINT files_pkey;
       public                 postgres    false    229            �           2606    18172    klamer klamer_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.klamer
    ADD CONSTRAINT klamer_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.klamer DROP CONSTRAINT klamer_pkey;
       public                 postgres    false    231            �           2606    18174    linear_panel linear_panel_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.linear_panel
    ADD CONSTRAINT linear_panel_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.linear_panel DROP CONSTRAINT linear_panel_pkey;
       public                 postgres    false    233            �           2606    18176    material material_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.material
    ADD CONSTRAINT material_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.material DROP CONSTRAINT material_pkey;
       public                 postgres    false    235            #           2606    18350    nest_file nest_file_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.nest_file
    ADD CONSTRAINT nest_file_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.nest_file DROP CONSTRAINT nest_file_pkey;
       public                 postgres    false    258            )           2606    18376    parts parts_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.parts
    ADD CONSTRAINT parts_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.parts DROP CONSTRAINT parts_pkey;
       public                 postgres    false    262            �           2606    18178    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public                 postgres    false    237                       2606    18180    profile profile_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.profile DROP CONSTRAINT profile_pkey;
       public                 postgres    false    239                       2606    18182    sheets sheets_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.sheets
    ADD CONSTRAINT sheets_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.sheets DROP CONSTRAINT sheets_pkey;
       public                 postgres    false    241                       2606    18184    task task_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.task DROP CONSTRAINT task_pkey;
       public                 postgres    false    243            
           2606    18186     task_products task_products_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.task_products
    ADD CONSTRAINT task_products_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.task_products DROP CONSTRAINT task_products_pkey;
       public                 postgres    false    245                       2606    18188 >   task_responsible_association task_responsible_association_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.task_responsible_association
    ADD CONSTRAINT task_responsible_association_pkey PRIMARY KEY (task_id, user_id);
 h   ALTER TABLE ONLY public.task_responsible_association DROP CONSTRAINT task_responsible_association_pkey;
       public                 postgres    false    247    247                       2606    18190 "   task_workshops task_workshops_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.task_workshops
    ADD CONSTRAINT task_workshops_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.task_workshops DROP CONSTRAINT task_workshops_pkey;
       public                 postgres    false    248            +           2606    18388    tools tools_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.tools
    ADD CONSTRAINT tools_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.tools DROP CONSTRAINT tools_pkey;
       public                 postgres    false    264                       2606    18192 8   user_workshop_association user_workshop_association_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.user_workshop_association
    ADD CONSTRAINT user_workshop_association_pkey PRIMARY KEY (user_id, workshop_id);
 b   ALTER TABLE ONLY public.user_workshop_association DROP CONSTRAINT user_workshop_association_pkey;
       public                 postgres    false    250    250                       2606    18194    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    251                       2606    18196    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    251                       2606    18198    users users_telegram_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_key UNIQUE (telegram);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_telegram_key;
       public                 postgres    false    251                       2606    18200    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    251                       2606    18202    weight weight_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.weight
    ADD CONSTRAINT weight_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.weight DROP CONSTRAINT weight_pkey;
       public                 postgres    false    253            !           2606    18204    workshop workshop_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.workshop
    ADD CONSTRAINT workshop_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.workshop DROP CONSTRAINT workshop_pkey;
       public                 postgres    false    255            �           1259    18205    fki_bracket_product_id_fkey    INDEX     U   CREATE INDEX fki_bracket_product_id_fkey ON public.bracket USING btree (product_id);
 /   DROP INDEX public.fki_bracket_product_id_fkey;
       public                 postgres    false    219            �           1259    18206    fki_cassette_product_id_fkey    INDEX     W   CREATE INDEX fki_cassette_product_id_fkey ON public.cassette USING btree (product_id);
 0   DROP INDEX public.fki_cassette_product_id_fkey;
       public                 postgres    false    221            �           1259    18207 %   fki_extension_bracket_product_id_fkey    INDEX     i   CREATE INDEX fki_extension_bracket_product_id_fkey ON public.extension_bracket USING btree (product_id);
 9   DROP INDEX public.fki_extension_bracket_product_id_fkey;
       public                 postgres    false    227            �           1259    18208     fki_linear_panel_product_id_fkey    INDEX     _   CREATE INDEX fki_linear_panel_product_id_fkey ON public.linear_panel USING btree (product_id);
 4   DROP INDEX public.fki_linear_panel_product_id_fkey;
       public                 postgres    false    233            �           1259    18209    fki_profile_product_id_fkey    INDEX     U   CREATE INDEX fki_profile_product_id_fkey ON public.profile USING btree (product_id);
 /   DROP INDEX public.fki_profile_product_id_fkey;
       public                 postgres    false    239                       1259    18210    fki_sheets_task_id_fkey    INDEX     M   CREATE INDEX fki_sheets_task_id_fkey ON public.sheets USING btree (task_id);
 +   DROP INDEX public.fki_sheets_task_id_fkey;
       public                 postgres    false    241                       1259    18211 -   fki_task_responsible_association_task_id_fkey    INDEX     y   CREATE INDEX fki_task_responsible_association_task_id_fkey ON public.task_responsible_association USING btree (task_id);
 A   DROP INDEX public.fki_task_responsible_association_task_id_fkey;
       public                 postgres    false    247            �           1259    18212    fki_л    INDEX     A   CREATE INDEX "fki_л" ON public.klamer USING btree (product_id);
    DROP INDEX public."fki_л";
       public                 postgres    false    231                       1259    18213    idx_weight_material_id    INDEX     P   CREATE INDEX idx_weight_material_id ON public.weight USING btree (material_id);
 *   DROP INDEX public.idx_weight_material_id;
       public                 postgres    false    253            �           1259    18214 	   ix_bid_id    INDEX     7   CREATE INDEX ix_bid_id ON public.bid USING btree (id);
    DROP INDEX public.ix_bid_id;
       public                 postgres    false    217            �           1259    18215    ix_bracket_id    INDEX     ?   CREATE INDEX ix_bracket_id ON public.bracket USING btree (id);
 !   DROP INDEX public.ix_bracket_id;
       public                 postgres    false    219            �           1259    18216    ix_cassette_id    INDEX     A   CREATE INDEX ix_cassette_id ON public.cassette USING btree (id);
 "   DROP INDEX public.ix_cassette_id;
       public                 postgres    false    221            �           1259    18217    ix_comment_id    INDEX     ?   CREATE INDEX ix_comment_id ON public.comment USING btree (id);
 !   DROP INDEX public.ix_comment_id;
       public                 postgres    false    223            �           1259    18218    ix_customer_id    INDEX     A   CREATE INDEX ix_customer_id ON public.customer USING btree (id);
 "   DROP INDEX public.ix_customer_id;
       public                 postgres    false    225            �           1259    18219    ix_extension_bracket_id    INDEX     S   CREATE INDEX ix_extension_bracket_id ON public.extension_bracket USING btree (id);
 +   DROP INDEX public.ix_extension_bracket_id;
       public                 postgres    false    227            �           1259    18220    ix_files_id    INDEX     ;   CREATE INDEX ix_files_id ON public.files USING btree (id);
    DROP INDEX public.ix_files_id;
       public                 postgres    false    229            �           1259    18221    ix_klamer_id    INDEX     =   CREATE INDEX ix_klamer_id ON public.klamer USING btree (id);
     DROP INDEX public.ix_klamer_id;
       public                 postgres    false    231            �           1259    18222    ix_linear_panel_id    INDEX     I   CREATE INDEX ix_linear_panel_id ON public.linear_panel USING btree (id);
 &   DROP INDEX public.ix_linear_panel_id;
       public                 postgres    false    233            �           1259    18223    ix_material_id    INDEX     A   CREATE INDEX ix_material_id ON public.material USING btree (id);
 "   DROP INDEX public.ix_material_id;
       public                 postgres    false    235            �           1259    18224    ix_product_id    INDEX     ?   CREATE INDEX ix_product_id ON public.product USING btree (id);
 !   DROP INDEX public.ix_product_id;
       public                 postgres    false    237            �           1259    18225    ix_profile_id    INDEX     ?   CREATE INDEX ix_profile_id ON public.profile USING btree (id);
 !   DROP INDEX public.ix_profile_id;
       public                 postgres    false    239                       1259    18226    ix_sheets_id    INDEX     =   CREATE INDEX ix_sheets_id ON public.sheets USING btree (id);
     DROP INDEX public.ix_sheets_id;
       public                 postgres    false    241                       1259    18227 
   ix_task_id    INDEX     9   CREATE INDEX ix_task_id ON public.task USING btree (id);
    DROP INDEX public.ix_task_id;
       public                 postgres    false    243                       1259    18228    ix_task_workshops_id    INDEX     M   CREATE INDEX ix_task_workshops_id ON public.task_workshops USING btree (id);
 (   DROP INDEX public.ix_task_workshops_id;
       public                 postgres    false    248                       1259    18229    ix_users_id    INDEX     ;   CREATE INDEX ix_users_id ON public.users USING btree (id);
    DROP INDEX public.ix_users_id;
       public                 postgres    false    251                       1259    18230    ix_workshop_id    INDEX     A   CREATE INDEX ix_workshop_id ON public.workshop USING btree (id);
 "   DROP INDEX public.ix_workshop_id;
       public                 postgres    false    255            ,           2606    18231    bid bid_customer_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.bid
    ADD CONSTRAINT bid_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);
 B   ALTER TABLE ONLY public.bid DROP CONSTRAINT bid_customer_id_fkey;
       public               postgres    false    217    4839    225            -           2606    18236    bracket bracket_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.bracket
    ADD CONSTRAINT bracket_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.bracket DROP CONSTRAINT bracket_product_id_fkey;
       public               postgres    false    237    219    4861            .           2606    18241 !   cassette cassette_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cassette
    ADD CONSTRAINT cassette_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 K   ALTER TABLE ONLY public.cassette DROP CONSTRAINT cassette_product_id_fkey;
       public               postgres    false    237    4861    221            C           2606    18365 1   clamp_locations clamp_locations_nest_file_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.clamp_locations
    ADD CONSTRAINT clamp_locations_nest_file_id_fkey FOREIGN KEY (nest_file_id) REFERENCES public.nest_file(id) ON DELETE CASCADE;
 [   ALTER TABLE ONLY public.clamp_locations DROP CONSTRAINT clamp_locations_nest_file_id_fkey;
       public               postgres    false    4899    260    258            /           2606    18246    comment comment_bid_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.bid(id) ON DELETE CASCADE;
 E   ALTER TABLE ONLY public.comment DROP CONSTRAINT comment_bid_id_fkey;
       public               postgres    false    223    4823    217            0           2606    18251    comment comment_user_id_fkey    FK CONSTRAINT     {   ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 F   ALTER TABLE ONLY public.comment DROP CONSTRAINT comment_user_id_fkey;
       public               postgres    false    251    4887    223            1           2606    18256 3   extension_bracket extension_bracket_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.extension_bracket
    ADD CONSTRAINT extension_bracket_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 ]   ALTER TABLE ONLY public.extension_bracket DROP CONSTRAINT extension_bracket_product_id_fkey;
       public               postgres    false    227    237    4861            2           2606    18261    files files_bid_id_fkey    FK CONSTRAINT     s   ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.bid(id);
 A   ALTER TABLE ONLY public.files DROP CONSTRAINT files_bid_id_fkey;
       public               postgres    false    217    229    4823            3           2606    18266    klamer klamer_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.klamer
    ADD CONSTRAINT klamer_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.klamer DROP CONSTRAINT klamer_product_id_fkey;
       public               postgres    false    4861    237    231            4           2606    18271 )   linear_panel linear_panel_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.linear_panel
    ADD CONSTRAINT linear_panel_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 S   ALTER TABLE ONLY public.linear_panel DROP CONSTRAINT linear_panel_product_id_fkey;
       public               postgres    false    237    4861    233            B           2606    18351     nest_file nest_file_file_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.nest_file
    ADD CONSTRAINT nest_file_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.files(id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.nest_file DROP CONSTRAINT nest_file_file_id_fkey;
       public               postgres    false    258    4846    229            D           2606    18377    parts parts_nest_file_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.parts
    ADD CONSTRAINT parts_nest_file_id_fkey FOREIGN KEY (nest_file_id) REFERENCES public.nest_file(id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.parts DROP CONSTRAINT parts_nest_file_id_fkey;
       public               postgres    false    258    4899    262            5           2606    18276    profile profile_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 I   ALTER TABLE ONLY public.profile DROP CONSTRAINT profile_product_id_fkey;
       public               postgres    false    239    4861    237            6           2606    18281    sheets sheets_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sheets
    ADD CONSTRAINT sheets_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.sheets DROP CONSTRAINT sheets_task_id_fkey;
       public               postgres    false    241    243    4872            7           2606    18286    task task_bid_id_fkey    FK CONSTRAINT     q   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.bid(id);
 ?   ALTER TABLE ONLY public.task DROP CONSTRAINT task_bid_id_fkey;
       public               postgres    false    4823    217    243            8           2606    18291    task task_material_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.material(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.task DROP CONSTRAINT task_material_id_fkey;
       public               postgres    false    235    243    4858            9           2606    18296 +   task_products task_products_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_products
    ADD CONSTRAINT task_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;
 U   ALTER TABLE ONLY public.task_products DROP CONSTRAINT task_products_product_id_fkey;
       public               postgres    false    4861    245    237            :           2606    18301 (   task_products task_products_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_products
    ADD CONSTRAINT task_products_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.task_products DROP CONSTRAINT task_products_task_id_fkey;
       public               postgres    false    243    245    4872            ;           2606    18306 F   task_responsible_association task_responsible_association_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_responsible_association
    ADD CONSTRAINT task_responsible_association_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE CASCADE;
 p   ALTER TABLE ONLY public.task_responsible_association DROP CONSTRAINT task_responsible_association_task_id_fkey;
       public               postgres    false    4872    247    243            <           2606    18311 F   task_responsible_association task_responsible_association_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_responsible_association
    ADD CONSTRAINT task_responsible_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 p   ALTER TABLE ONLY public.task_responsible_association DROP CONSTRAINT task_responsible_association_user_id_fkey;
       public               postgres    false    251    247    4887            =           2606    18316 *   task_workshops task_workshops_task_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_workshops
    ADD CONSTRAINT task_workshops_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.task_workshops DROP CONSTRAINT task_workshops_task_id_fkey;
       public               postgres    false    248    243    4872            >           2606    18321 .   task_workshops task_workshops_workshop_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.task_workshops
    ADD CONSTRAINT task_workshops_workshop_id_fkey FOREIGN KEY (workshop_id) REFERENCES public.workshop(id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.task_workshops DROP CONSTRAINT task_workshops_workshop_id_fkey;
       public               postgres    false    255    248    4897            E           2606    18389    tools tools_nest_file_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tools
    ADD CONSTRAINT tools_nest_file_id_fkey FOREIGN KEY (nest_file_id) REFERENCES public.nest_file(id) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.tools DROP CONSTRAINT tools_nest_file_id_fkey;
       public               postgres    false    264    4899    258            ?           2606    18326 @   user_workshop_association user_workshop_association_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_workshop_association
    ADD CONSTRAINT user_workshop_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 j   ALTER TABLE ONLY public.user_workshop_association DROP CONSTRAINT user_workshop_association_user_id_fkey;
       public               postgres    false    4887    250    251            @           2606    18331 D   user_workshop_association user_workshop_association_workshop_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_workshop_association
    ADD CONSTRAINT user_workshop_association_workshop_id_fkey FOREIGN KEY (workshop_id) REFERENCES public.workshop(id);
 n   ALTER TABLE ONLY public.user_workshop_association DROP CONSTRAINT user_workshop_association_workshop_id_fkey;
       public               postgres    false    250    255    4897            A           2606    18336    weight weight_material_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.weight
    ADD CONSTRAINT weight_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.material(id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.weight DROP CONSTRAINT weight_material_id_fkey;
       public               postgres    false    253    235    4858            �   L   x�3��4�0�4��t����s��s�21
���Â<}��\�!▜�f ����@��a`QS#NKt�=... �g�      �      x�3�45 !CS����\1z\\\ -g      �      x���43�������� �R            x������ � �      �      x������ � �      �   _   x�ʻ	�@ �x�
+�����`�x zX�lG��<�6n����k-Ɇ�2��|��'���A+av�H�ѧ[kaa͘��9rh���;�<      �      x������ � �      �   K   x�340�41�0�000��K�"�Ă�����Լ0�� '?1�X��\�����IgAJ'���+F��� Qr"O      �      x������ � �      �      x������ � �      �      x�31���s���s�������� 0�              x������ � �            x������ � �      �   /   x�3���w��q�25�t
rt�v�23�tvv	q����� ��      �      x�34�4��t71�01�4600������ 1:�      �      x������ � �      �   F   x�31�4��41��uu��������4202�50�54U04�21�24ӳ4��43�60������� ���      �   "   x�3��41�43���445�4�L2�b���� EU�      �      x������ � �      �   A   x�33�41�44������4�23�r���{�����,�Bf�B�`!s$!s���P� ߬]            x������ � �      �   5   x�%ʹ  �����r|���L`9�]��);�8)��?p��+�H��:�      �   y  x�U��N�@ �������c[�R
��pi�B��t��/&z�b��' DE��o�"h4�Lvf��f�4 ��l�'y'+��}|E��m}�l4�O@2�$�L2-�� �u����bY�hu2���͢ޓq�4z���_Д�Ջ#�����`Y@��B6����9^�/i���ic�[� #�:�=�1�Ad֔�}b��^T<=�i��B�5�U�q��4,5�j�R��x\1��䉬���&����߱4ݣs��(�Um=[���4D>{.w��M!l&��G��˧�G.g���9Mp�`�+��Ne3 �އ=��=�CuX��Y�-IcѬ�23aOQ�����,��0U�}����F���6�H$� �t�N      �      x������ � �      �   k   x�=�K�0E���b�?MãX-N\�R�� fWGW����l��b�ӃMt���<1D��+�O+��� �h��{�@����'�%������\����������ވ���!     