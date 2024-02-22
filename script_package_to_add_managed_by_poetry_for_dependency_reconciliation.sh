#!/bin/bash

## Adding packaged and getting poetry to reconcile dependencies
llm_chat_embed_venv/bin/poetry add absl-py accelerate aiohttp aiosignal anyascii anyio asttokens astunparse async-timeout attrs audioread Babel bangla blinker bnnumerizer bnunicodenormalizer cachetools catalogue cli_helpers click confection configobj contourpy coqpit cycler cymem Cython dataclasses-json dateparser decorator dill docopt einops encodec executing faster-whisper ffmpeg-python Flask Flask-Cors fonttools frozenlist future g2pkk gast google-auth google-auth-oauthlib google-pasta graphviz greenlet grpcio h5py hangul-romanize huggingface-cli inflect inquirerpy ipython itsdangerous jamo jedi jieba Jinja2 joblib jsonlines jsonpatch jsonpointer keras kiwisolver langchain langchain-community langchain-core langchain-openai langcodes langsmith lazy_loader libclang librosa llvmlite Markdown MarkupSafe marshmallow matplotlib matplotlib-inline ml-dtypes msgpack multidict multiprocess murmurhash mypy-extensions nltk num2words numba numpy
llm_chat_embed_venv/bin/poetry add nvidia-cublas-cu12==12.1.3.1 nvidia-cuda-cupti-cu12==12.1.105 nvidia-cuda-nvrtc-cu12==12.1.105 nvidia-cuda-runtime-cu12==12.1.105 nvidia-cudnn-cu12==8.9.2.26 nvidia-cufft-cu12==11.0.2.54 nvidia-curand-cu12==10.3.2.106 nvidia-cusolver-cu12==11.4.5.107 nvidia-cusparse-cu12==12.1.0.106 nvidia-nccl-cu12==2.19.3 nvidia-nvjitlink-cu12==12.3.101 nvidia-nvtx-cu12==12.1.105
llm_chat_embed_venv/bin/poetry add oauthlib opt-einsum pandas parso pendulum pexpect pfzy pgcli pgspecial pgvector pillow platformdirs pooch preshed prompt-toolkit psutil psycopg psycopg2 psycopg2-binary ptyprocess pure-eval pyarrow pyarrow-hotfix pyasn1 pyasn1-modules PyAudio pyttsx3 pydot Pygments pynndescent pyparsing pypinyin pysbd python-crfsuite python-dateutil python-dotenv pytz regex requests-oauthlib rsa safetensors scipy sentencepiece setproctitle six smart-open soundfile soxr spacy spacy-legacy spacy-loggers SQLAlchemy sqlparse srsly stack-data SudachiDict-core SudachiPy tabulate tenacity tensorboard tensorboard-data-server tensorflow-estimator tensorflow-io-gcs-filesystem termcolor tf-keras threadpoolctl tiktoken time-machine tokenizers torch torchaudio trainer traitlets transformers triton typer typing-inspect tzdata tzlocal umap-learn Unidecode wasabi wcwidth Werkzeug wrapt xxhash yarl
llm_chat_embed_venv/bin/poetry add networkx>=2.8.8,<3.0.0 scikit-learn==1.4.1.post1 gruut>=2.3.4,<3.0.0 gruut-ipa gruut-lang-de gruut-lang-en gruut-lang-es gruut-lang-fr tensorflow==2.15.0.post1
llm_chat_embed_venv/bin/poetry add datasets>=2.17.1,<3.0.0 fsspec>=2023.1.0,<=2023.10.0 TTS==0.21.1
llm_chat_embed_venv/bin/poetry add weasel==0.3.4 cloudpathlib==0.16.0 trainer==0.0.36
llm_chat_embed_venv/bin/poetry add blis==0.7.11 thinc==8.2.3
llm_chat_embed_venv/bin/poetry add httpx<0.26.0 ollama==0.1.6
