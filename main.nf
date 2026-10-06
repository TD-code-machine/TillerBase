nextflow.enable.dsl=2

include { FASTQC } from './modules/fastqc'
include { MULTIQC } from './modules/multiqc'

params.reads = null
params.outdir = 'results'

workflow {
    if (!params.reads) {
        log.info 'No reads supplied. Use --reads "data/*_{1,2}.fastq.gz" for real data.'
        return
    }

    reads_ch = Channel.fromFilePairs(params.reads, checkIfExists: true)
    FASTQC(reads_ch)
    MULTIQC(FASTQC.out.reports.collect())
}
