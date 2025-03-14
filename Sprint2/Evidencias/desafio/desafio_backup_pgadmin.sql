PGDMP  1    	                |            desafio_sprint2    16.3    16.3      $           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            %           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            &           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            '           1262    34100    desafio_sprint2    DATABASE     �   CREATE DATABASE desafio_sprint2 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE desafio_sprint2;
                postgres    false            �            1259    34115    carro    TABLE     �   CREATE TABLE public.carro (
    idcarro integer NOT NULL,
    classicarro text NOT NULL,
    marcacarro text NOT NULL,
    modelocarro text NOT NULL,
    anocarro integer NOT NULL,
    id_combustivelfk integer
);
    DROP TABLE public.carro;
       public         heap    postgres    false            �            1259    34101    cliente    TABLE     �   CREATE TABLE public.cliente (
    idcliente integer NOT NULL,
    nomecliente text NOT NULL,
    cidadecliente text NOT NULL,
    estadocliente text NOT NULL,
    paiscliente text NOT NULL
);
    DROP TABLE public.cliente;
       public         heap    postgres    false            �            1259    34108    combustivel    TABLE     k   CREATE TABLE public.combustivel (
    idcombustivel integer NOT NULL,
    tipocombustivel text NOT NULL
);
    DROP TABLE public.combustivel;
       public         heap    postgres    false            �            1259    34127    quilometragem    TABLE     �   CREATE TABLE public.quilometragem (
    id_km integer NOT NULL,
    kmcarro integer NOT NULL,
    id_carrokm_fk integer NOT NULL
);
 !   DROP TABLE public.quilometragem;
       public         heap    postgres    false            �            1259    34181    dimensao_carro    VIEW     �  CREATE VIEW public.dimensao_carro AS
 WITH ultima_quilometragem AS (
         SELECT quilometragem.id_carrokm_fk,
            max(quilometragem.kmcarro) AS kmcarro
           FROM public.quilometragem
          GROUP BY quilometragem.id_carrokm_fk
        )
 SELECT c.idcarro AS codigo,
    q.kmcarro AS quilometragem,
    c.classicarro AS classificacao,
    c.marcacarro AS marca,
    c.modelocarro AS modelo,
    c.anocarro AS ano,
    cb.tipocombustivel
   FROM ((public.carro c
     JOIN public.combustivel cb ON ((c.id_combustivelfk = cb.idcombustivel)))
     JOIN ultima_quilometragem q ON ((q.id_carrokm_fk = c.idcarro)))
  ORDER BY c.idcarro;
 !   DROP VIEW public.dimensao_carro;
       public          postgres    false    216    217    217    217    216    217    217    217    218    218            �            1259    34169    dimensao_cliente    VIEW     �   CREATE VIEW public.dimensao_cliente AS
 SELECT idcliente AS codigo,
    nomecliente AS nome,
    cidadecliente AS cidade,
    estadocliente AS estado,
    paiscliente AS pais
   FROM public.cliente;
 #   DROP VIEW public.dimensao_cliente;
       public          postgres    false    215    215    215    215    215            �            1259    34144    locacao    TABLE     j  CREATE TABLE public.locacao (
    idlocacao integer NOT NULL,
    datalocacao date NOT NULL,
    horalocacao time without time zone NOT NULL,
    qtddiaria integer NOT NULL,
    vlrdiaria real NOT NULL,
    dataentrega date NOT NULL,
    horaentrega time without time zone NOT NULL,
    id_clientefk integer,
    id_vendedorfk integer,
    id_carrofk integer
);
    DROP TABLE public.locacao;
       public         heap    postgres    false            �            1259    34164    dimensao_tempo    VIEW     �  CREATE VIEW public.dimensao_tempo AS
 SELECT DISTINCT locacao.datalocacao AS data,
    EXTRACT(year FROM locacao.datalocacao) AS ano,
    EXTRACT(month FROM locacao.datalocacao) AS mes,
    EXTRACT(day FROM locacao.datalocacao) AS dia,
    EXTRACT(week FROM locacao.datalocacao) AS semana,
    locacao.horalocacao AS hora
   FROM public.locacao
UNION
 SELECT DISTINCT locacao.dataentrega AS data,
    EXTRACT(year FROM locacao.dataentrega) AS ano,
    EXTRACT(month FROM locacao.dataentrega) AS mes,
    EXTRACT(day FROM locacao.dataentrega) AS dia,
    EXTRACT(week FROM locacao.dataentrega) AS semana,
    locacao.horaentrega AS hora
   FROM public.locacao
  ORDER BY 1;
 !   DROP VIEW public.dimensao_tempo;
       public          postgres    false    220    220    220    220            �            1259    34137    vendedor    TABLE     �   CREATE TABLE public.vendedor (
    idvendedor integer NOT NULL,
    nomevendedor text NOT NULL,
    sexovendedor text NOT NULL,
    estadovendedor text NOT NULL
);
    DROP TABLE public.vendedor;
       public         heap    postgres    false            �            1259    34173    dimensao_vendedor    VIEW     �   CREATE VIEW public.dimensao_vendedor AS
 SELECT idvendedor AS codigo,
    nomevendedor AS nome,
    sexovendedor AS sexo,
    estadovendedor AS estado
   FROM public.vendedor l;
 $   DROP VIEW public.dimensao_vendedor;
       public          postgres    false    219    219    219    219            �            1259    34177    fato_locacao    VIEW     E  CREATE VIEW public.fato_locacao AS
 SELECT idlocacao AS codigo,
    datalocacao,
    horalocacao,
    qtddiaria AS quantidadediaria,
    vlrdiaria AS valordiaria,
    dataentrega,
    horaentrega,
    id_clientefk AS codigocliente,
    id_carrofk AS codigocarro,
    id_vendedorfk AS codigovendedor
   FROM public.locacao l;
    DROP VIEW public.fato_locacao;
       public          postgres    false    220    220    220    220    220    220    220    220    220    220                      0    34115    carro 
   TABLE DATA           j   COPY public.carro (idcarro, classicarro, marcacarro, modelocarro, anocarro, id_combustivelfk) FROM stdin;
    public          postgres    false    217   -                 0    34101    cliente 
   TABLE DATA           d   COPY public.cliente (idcliente, nomecliente, cidadecliente, estadocliente, paiscliente) FROM stdin;
    public          postgres    false    215   �-                 0    34108    combustivel 
   TABLE DATA           E   COPY public.combustivel (idcombustivel, tipocombustivel) FROM stdin;
    public          postgres    false    216   �.       !          0    34144    locacao 
   TABLE DATA           �   COPY public.locacao (idlocacao, datalocacao, horalocacao, qtddiaria, vlrdiaria, dataentrega, horaentrega, id_clientefk, id_vendedorfk, id_carrofk) FROM stdin;
    public          postgres    false    220   $/                 0    34127    quilometragem 
   TABLE DATA           F   COPY public.quilometragem (id_km, kmcarro, id_carrokm_fk) FROM stdin;
    public          postgres    false    218   i0                  0    34137    vendedor 
   TABLE DATA           Z   COPY public.vendedor (idvendedor, nomevendedor, sexovendedor, estadovendedor) FROM stdin;
    public          postgres    false    219   �0       |           2606    34121    carro carro_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.carro
    ADD CONSTRAINT carro_pkey PRIMARY KEY (idcarro);
 :   ALTER TABLE ONLY public.carro DROP CONSTRAINT carro_pkey;
       public            postgres    false    217            x           2606    34107    cliente cliente_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (idcliente);
 >   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_pkey;
       public            postgres    false    215            z           2606    34114    combustivel combustivel_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.combustivel
    ADD CONSTRAINT combustivel_pkey PRIMARY KEY (idcombustivel);
 F   ALTER TABLE ONLY public.combustivel DROP CONSTRAINT combustivel_pkey;
       public            postgres    false    216            �           2606    34148    locacao locacao_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.locacao
    ADD CONSTRAINT locacao_pkey PRIMARY KEY (idlocacao);
 >   ALTER TABLE ONLY public.locacao DROP CONSTRAINT locacao_pkey;
       public            postgres    false    220            ~           2606    34131     quilometragem quilometragem_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.quilometragem
    ADD CONSTRAINT quilometragem_pkey PRIMARY KEY (id_km);
 J   ALTER TABLE ONLY public.quilometragem DROP CONSTRAINT quilometragem_pkey;
       public            postgres    false    218            �           2606    34143    vendedor vendedor_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.vendedor
    ADD CONSTRAINT vendedor_pkey PRIMARY KEY (idvendedor);
 @   ALTER TABLE ONLY public.vendedor DROP CONSTRAINT vendedor_pkey;
       public            postgres    false    219            �           2606    34122 !   carro carro_id_combustivelfk_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.carro
    ADD CONSTRAINT carro_id_combustivelfk_fkey FOREIGN KEY (id_combustivelfk) REFERENCES public.combustivel(idcombustivel);
 K   ALTER TABLE ONLY public.carro DROP CONSTRAINT carro_id_combustivelfk_fkey;
       public          postgres    false    217    4730    216            �           2606    34159    locacao locacao_id_carrofk_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.locacao
    ADD CONSTRAINT locacao_id_carrofk_fkey FOREIGN KEY (id_carrofk) REFERENCES public.carro(idcarro);
 I   ALTER TABLE ONLY public.locacao DROP CONSTRAINT locacao_id_carrofk_fkey;
       public          postgres    false    217    4732    220            �           2606    34149 !   locacao locacao_id_clientefk_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.locacao
    ADD CONSTRAINT locacao_id_clientefk_fkey FOREIGN KEY (id_clientefk) REFERENCES public.cliente(idcliente);
 K   ALTER TABLE ONLY public.locacao DROP CONSTRAINT locacao_id_clientefk_fkey;
       public          postgres    false    4728    215    220            �           2606    34154 "   locacao locacao_id_vendedorfk_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.locacao
    ADD CONSTRAINT locacao_id_vendedorfk_fkey FOREIGN KEY (id_vendedorfk) REFERENCES public.vendedor(idvendedor);
 L   ALTER TABLE ONLY public.locacao DROP CONSTRAINT locacao_id_vendedorfk_fkey;
       public          postgres    false    4736    220    219            �           2606    34132 .   quilometragem quilometragem_id_carrokm_fk_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.quilometragem
    ADD CONSTRAINT quilometragem_id_carrokm_fk_fkey FOREIGN KEY (id_carrokm_fk) REFERENCES public.carro(idcarro);
 X   ALTER TABLE ONLY public.quilometragem DROP CONSTRAINT quilometragem_id_carrokm_fk_fkey;
       public          postgres    false    218    217    4732               �   x����
�@ ���S��?����I�M+貄A\P;���v� �2��aFD��l��"�.<<��U�+���`��!�.���Z+��6�4PF��4�>!��7��T� FyZ�л���0�!�B~v��8�u3���1��"���Q��\�(�8��;ꇞ�z�]���6�ԃG�巾d���6�u>��!OLcu         �   x�m��N�0���S�	t�{W�!�I�r1��,e�{ĉ�苑Tk6VNq����۵i-������-��h�\yT�բ�����	��{���4�E�1̱�UEձ��l�aT���(uSJ�Wd��s��'�䑋����/G���M�i��3���(��0|� ����/�#n����{�-�ɢ�M�E[ԋ�z<�c���Ŵ���l9�ǥ[�&��3�ZT�������_ֽ��         1   x�3�tO,����K�2�t-I����2�t�I��2�t�L-N������ ��5      !   5  x���]n� F�g{/S�?ӵt��(�&�P)B��N���W���øH�m�"{�ԔeE�L&�ɝE����Ʋ�H�Z�t�q�|c����c��^��Du�2b�d��r����BJ��jzf�0���<�>X}�������?]��{A�+���d�^؊LYcV$8��Wz���"�
c
)�/9��v+B����r9��˼r=��˲��[֕�Y���A��WF8ʞ\�V�Y2stFO��>Cy���#�����`�s�M�V���?K��r`�\Np`�,GXX,�A�a{/f���{         �   x�5��1г)�����鿎�dNOH,&8�Afn�U�5�(GG1l����&�����HG�;֌D�C!�a@�il��D����rB�p7���T��K�&B��֚&A��o�	����:��*??3���+9          �   x�]�M
�@FדS��Z�يA(�WnB'�@;��馷�ҋ9-�V�y/ߗ�̃�e�kq���T�[�F]���)a`	&_�����]-��W8����(�Q�{� �R��zSIfN-��<(�E�^\�Dǒ��4F�Xu����]��3�^PlW�̆�饒��!�7��}�\�     