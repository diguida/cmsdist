### RPM external fftw3 3.3.2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.fftw.org/fftw-%realversion.tar.gz

%prep
%setup -n fftw-%realversion

%build
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" \
   ./configure --with-pic --enable-shared --enable-sse2 --enable-threads \
     --disable-dependency-tracking --disable-fortran --disable-mpi --disable-openmp \
     --prefix=%i --host=x86_64-k1om-linux
     ;;
   * )
   ./configure --with-pic --enable-shared --enable-sse2 --enable-threads \
     --disable-dependency-tracking --disable-fortran --disable-mpi --disable-openmp \
     --prefix=%i
     ;;
esac
make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Remove documentation. 
%define drop_files %i/share
rm -rf %i/lib/*.la
