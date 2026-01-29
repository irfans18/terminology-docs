# X. CHANGELOG

**20260112**

- Penambahan parameter `alteplase`, `kantong_darah`, `apgar`, dan `persalinan` pada response method `get_claim_data` dengan kondisi tertentu.

**20251117**

- Penambahan Kode Error ungroupable iDRG

**20251023**

- Perubahan Alur Integrasi
- Penambahan Daftar Kode Ungroupable And Unrelated
- Perubahan parameter method `set_claim_data`
- Perubahan parameter method `grouper`
- Penambahan method `idrg_procedure_set`
- Penambahan method `idrg_procedure_get`
- Penambahan method `idrg_diagnose_seta`
- Penambahan method `idrg_diagnose_get`
- Penambahan method `idrg_grouper_final`
- Penambahan method `idrg_grouper_reedit`
- Penambahan method `idrg_to_inacbg_import`
- Penambahan method `inacbg_procedure_set`
- Penambahan method `inacbg_procedure_get`
- Penambahan method `inacbg_diagnose_set`
- Penambahan method `inacbg_diagnose_get`
- Penambahan method `inacbg_grouper_final`
- Penambahan method `inacbg_grouper_reedit`
- Drop method `pull_claim` (deprecated)

**20240701**

- Penambahan element `shk`
- Penambahan element `alteplase_ind`

**20230106**

- Koreksi method `sitb_validate` dan `sitb_invalidate`
- Bagan alur integrasi SITB

**20221221**

- Penambahan method `sitb_validate`
- Penambahan method `sitb_invalidate`

**20220108**

- Penambahan error code `E2063`

**20220104**

- Penambahan method `search_diagnosis_inagrouper`
- Penambahan method `search_procedures_inagrouper`
- Penambahan parameter `diagnosa_inagrouper` pada method `set_claim_data`
- Penambahan parameter `procedure_inagrouper` pada method `set_claim_data`

**20210607**

- Penambahan `payor_id` 72 s/d 75
- Parameter `payor_id` menjadi mandatory untuk method `set_claim_data`
- Penambahan jenis kartu identitas (`no_kartu_t`)
- Penambahan parameter `isoman_ind`
- Penambahan parameter `terapi_konvalesen`
- Penambahan parameter `akses_naat`

**20200727**

- Penambahan jenis kartu identitas (`no_kartu_t`)
- Penambahan parameter `covid19_rs_darurat_ind`
- Penambahan parameter `covid19_co_insidense_ind`
- Penambahan parameter `covid19_penunjang_pengurang`

**20200326**

- Penambahan Jaminan untuk pasien COVID-19
- Penambahan methode `generate_claim_number` untuk nomor pengajuan claim COVID-19 - Fix ketika error grouper, jenis rawat di hasil grouper selalu rawat jalan

**20190116**

- Fix error `set_claim_data` untuk rawat jalan poli eksekutif
- Penambahan parameter `tarif_poli_eks` di method `get_claim_data`

**20190114**

- Penambahan error code `E2032`
- Perubahan aturan naik kelas dibatasi hanya 1 tingkat diatas.
- Penambahan variable `obat_kronis` dan `obat_kemoterapi` pada `set_claim_data` dan `get_claim_data`.

**20171130**

- Update hasil `get_claim_data` untuk menampilkan format `tarif_rs`.

**20171128**

- Penambahan parameter tarif breakdown pada `set_claim_data`.
- Breakdown parameter `tarif_rs` pada `set_claim_data`.
- Pada method `send_claim`, parameter `jenis_rawat` ada penambahan value yaitu "3" (tiga) untuk rawat inap dan rawat jalan
- Pada method `send_claim` sekarang bisa memilih tanggal pulang atau tanggal grouping yaitu dengan penambahan parameter `date_type`, yaitu untuk menentukan bahwa parameter `start_dt` dan `stop_dt` adalah tanggal pulang atau tanggal grouping

**20170712**

- Fix "Error tidak diketahui" menjadi "Error key mismatch" untuk response `KEY_MISMATCH`

**20170605**

- Fix gender pada method `get_claim_data`
- Penambahan method `search_diagnosis`
- Penambahan method `search_procedures`
- Koreksi typo pada method `delete_patient`
- Fix bug `new_claim` ketika pasien sudah dihapus
- Fix `delete_patient` untuk no rm yang sama

**20170518**

- Penambahan katalog fungsi enkripsi / dekripsi dalam beberapa bahasa pemrograman di bagian akhir manual web service
- Refactoring, fungsi php `mc_*` menjadi `inacbg_*`
- Koreksi manual web service untuk naik kelas vvip
- Penambahan konfigurasi `enable_debug` di `server.ini` pada segment `[web_service]` untuk security

**20170511**

- Penambahan error code `E2030` Parameter tidak lengkap, sebagai response web service yang tidak menyertakan salah satu parameter yang dibutuhkan (mandatory)

**20170405**

- Penambahan parameter `cob_cd` pada method `set_claim_data`

**20170320**

- Penambahan error code `E2029` dan `E2099`
- Penambahan info jika terjadi kegagalan koneksi ketika `send_claim_individual`

**20170316**

- Penambahan parameter `add_payment_pct` pada method `set_claim_data`
- Penambahan result parameter `add_payment_amt` pada method grouper dan `get_claim_data`

**20161219**

- Penambahan kode error (`error_no`) pada setiap reponse dengan kesalahan
- Penambahan check duplikasi nomor sep untuk setiap method yang menggunakan nomor sep
- Penyeragaman format json variable hasil grouper dan `get_claim_data`
- Penambahan informasi `patient_id`, `admission_id` dan `hospital_admission_id` untuk response `new_claim` dan `get_claim_data`

**20161216**

- Penambahan method `claim_print`.
- Penambahan informasi tarif kelas 1,2 dan 3 untuk setiap response grouper dan `get_claim_data`. Dengan perubahan ini dimohon untuk setiap simrs yang telah melakukan integrasi sebelum ini untuk menyesuaikan kembali dengan format yang baru.
- Fix kode cara pulang (5 = Lain-lain) pada cetak klaim individual dan txt.
- Fix method grouper untuk klaim yang telah dihapus.
- Fix untuk `set_claim_data` pada saat grouper telah terfinal.
- Perubahan tanda delimiter untuk diagnosa dan prosedur pada method `get_claim_data` yang sebelumnya semicolon (;) menjadi hash (#).

**20161212**

- Penambahan parameter untuk ubah `nomor_kartu` pada method `set_claim_data`
- Penambahan parameter untuk naik kelas: `upgrade_class_ind`, `upgrade_class_class` dan `upgrade_class_los` pada method `set_claim_data`

**20161123**

- Penambahan method `send_claim_individual`
- Perubahan json response untuk `send_claim` untuk key "List" menjadi "data"
- Penyeragaman format encrypted/non-encrypted untuk masing-masing mode

**20161116**

- Penambahan method `get_claim_status`

**20161111**

- Penambahan envelope key untuk encryption dengan DC Kemkes
- Pemisahan key untuk pull_claim oleh client BPJS

**20161020**

- Penambahan flag untuk poli eksekutif

**20160514**

- Fix mandatory `coder_nik` di `new_claim` masih bisa tembus, dan set NIK internal user supaya kosong

**20160511**

- Encryption & Decryption dan mode debug untuk development
- Update manual

**20160502**

- Waktu grouping adalah waktu yg dicatat ketika pemanggilan method `set_claim_data`, grouper dan `claim_final`. Untuk NIK Coder hanya dicatat pada pemanggilan method `set_claim_data`.
- NIK Coder sekarang mandatory dalam method `set_claim_data`, dan NIK tersebut harus teregister dalam data user.
- Fix penambahan kode ICD10 dan ICD9CM yang masih belum ada.
- Status Klaim "Siap" dihilangkan, diganti "Final" supaya lebih simple.
- Gender pada method `new_claim` dan `update_patient` berubah dari L/P menjadi 1 = Laki / 2 = Perempuan.
- Penambahan method `delete_claim`.
- Penambahan method `delete_patient`.
- Penambahan method `update_patient`.
- Penambahan method `get_claim_data`.
- Untuk `set_claim_data` ada penambahan metadata `nomor_sep` sebagai identifier, sedangkan yang `nomor_sep` didalam data adalah sebagai nilai perubahan jika akan dilakukan perubahan.
- Fix rounding tarif sub acute dan chronic.
- Penambahan kode cbg `X-0-99-X FAILED: EMPTY RESPONSE`, supaya lebih informatif untuk kasus UNU Grouper crash. Terkait juga dengan hasil grouping minus.
- Fix bug nama dengan single quote untuk simpan melalui ws

**20160421**

- Fix grouping untuk special CMG lebih dari 1.
- Fix error unduh data.
- Fix error untuk `nomor_sep` beda dalam 1 pasien.
