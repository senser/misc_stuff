    def pack(self, name, dir, filter=None, targetdir=None):
        if not targetdir:
            targetdir = dir
        filename = "{0}{1}".format(name, self.package_file_ext)
        filepath = os.path.join(targetdir, filename)

        self.create_meta(dir, name, filter=filter)
        # Create file list before creating tarball to exclude tarball from file list
        files = [(f, os.path.relpath(f, dir)) for f in self.file_iter(dir, filter=filter)]

        try:
#            tar = tarfile.open(filepath, mode="w:gz")
            tar = tarfile.open(filepath, mode="w:gz", compresslevel=6)
#            tar = tarfile.open(filepath, mode="w")

            for path, rel_path in files:
######### original variant - 70 secs #############
                tar.add(path, arcname=rel_path, recursive=False)
######### alternative variant - 70 secs #############
#                tarinfo = tar.gettarinfo(path, rel_path)
#                if tarinfo:
#                    if tarinfo.isreg():
#                        with open(path, "rb") as f:
#                            tar.addfile(tarinfo, f)
#                    else:
#                        tar.addfile(tarinfo)
            tar.close()
######### compress tar file by calling gzip in shell - 29 secs ######
#            os.system('gzip -f %s' % filepath)
######### compress tar file with gzip module - 70 secs ########
#            f_in = open(filepath, 'rb')
#            f_out = gzip.open('%s.gz' % filepath, 'wb')
#            shutil.copyfileobj(f_in, f_out)
#            f_in.close()
#            f_out.close()
#####################################################
######### compress tar file with zlib module - 31 secs ########
#            f_in = open(filepath, 'rb')
#            f_out = open('%s.gz' % filepath, 'wb')
#            # write gzip header
#            statval = os.stat(filepath)
#            f_out.write('\037\213')                            # magic header
#            f_out.write('\010')                                # compression method
#            f_out.write(chr(8))                                # flag byte
#            f_out.write(struct.pack("<L", long(statval[8])))   # modification time
#            f_out.write('\002')                                # slowest compression alg
#            f_out.write('\377')                                # OS (=unknown)
#            f_out.write(filepath + '\000')                     # original filename
#            crcval = zlib.crc32("") & 0xffffffffL
#            compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
#            # compress file
#            while True:
#                data = f_in.read(1024)
#                if data == '':
#                    break
#                crcval = zlib.crc32(data, crcval) & 0xffffffffL
#                f_out.write(compressor.compress(data))
#            f_out.write(compressor.flush())
#            # finish file
#            f_out.write(struct.pack("<L", crcval))
#            f_out.write(struct.pack("<L", statval[6] & 0xffffffffL))
#            f_in.close()
#            f_out.close()
#####################################################
        except IOError as e:
            raise PackagerError(e)
        os.remove(os.path.join(dir, self.meta_file_name))
        return filepath
