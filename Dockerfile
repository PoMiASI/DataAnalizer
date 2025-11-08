FROM continuumio/miniconda3

WORKDIR /workspace

# Copy environment spec and create the conda environment
COPY environment.yml /workspace/environment.yml
RUN conda env create -f /workspace/environment.yml && \
    conda clean -afy

# Use the created environment for subsequent RUN/CMD instructions
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-lc"]

# Ensure environment binaries are on PATH
ENV PATH /opt/conda/envs/myenv/bin:$PATH

EXPOSE 8888

# Default command
CMD ["bash"]
