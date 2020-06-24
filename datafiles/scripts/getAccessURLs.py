
jobnrs = [125,126,127,128]


for jobnr in jobnrs :
  
  filename = "job{0}_{1}_completed_accessURLs.txt".format(jobnr,jobs(jobnr).name).replace("/","_")
  print ("\nWriting accessURLs to {0}".format(filename))

  f = open(filename, "w")
  for job in jobs(jobnr).subjobs.select(status='completed') :
    files = job.backend.getOutputDataAccessURLs()
    for ifile in files :
      if not "histos" in ifile :
        print(ifile)
        f.write(ifile + "\n")

  f.close()

