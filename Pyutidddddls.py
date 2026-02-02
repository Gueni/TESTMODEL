

    def process_standalone_csvs(self, fileLog, saveMode='w'):

        ts_dir  = f"{fileLog.resultfolder}/CSV_TIME_SERIES"
        map_dir = f"{fileLog.resultfolder}/CSV_MAPS"

        files = sorted(f for f in os.listdir(ts_dir) if f.endswith("_Standalone.csv"))
        if not files: return

        results = { "RMS": [], "AVG": [], "MAX": [], "FFT": [] }

        for f in files:
            data   = dp.pd.read_csv(os.path.join(ts_dir, f)).to_numpy(dp.np.float64)
            T_vect = data[:, 0]
            sigs   = data[:, 1:].T

            [results[k].append(self.operation(T_vect, sigs, m).tolist()) for k, m in (("RMS",4),("AVG",5),("MAX",1))]

            results["FFT"] += self.postProcessing.FFT_mat(T_vect, sigs).tolist()

        # ---- write MAP CSVs ----
        for k, v in results.items(): self.postProcessing.csv_append_rows(f"{map_dir}/Standalone_{k}_Map.csv",v,save_mode=saveMode)


   