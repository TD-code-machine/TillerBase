process FASTQC {
    tag "$sample_id"
    publishDir "${params.outdir}/fastqc", mode: 'copy'

    input:
    tuple val(sample_id), path(reads)

    output:
    path "*_fastqc.zip", emit: reports
    path "*_fastqc.html", emit: html

    script:
    """
    fastqc --threads ${task.cpus} ${reads}
    """
}
