using System.Diagnostics;
using System.Security.Cryptography;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using MVC2.Data;
using MVC2.Models;
using static IronPython.Modules._ast;
using IronPython.Hosting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using static Community.CsharpSqlite.Sqlite3;

namespace MVC2.Controllers
{
	public class EmployeesController : Controller
	{
		ApplicationDbContext _context ;
		IWebHostEnvironment _WebHostEnvironment;

		public EmployeesController(IWebHostEnvironment web,ApplicationDbContext context)
		{
			_context = context;
			_WebHostEnvironment = web;
		}

		[HttpPost]
        public IActionResult AddNew(Employee emp, IFormFile? mediaFile)
        {
            if (mediaFile != null)
            {
                string fileExtension = Path.GetExtension(mediaFile.FileName).ToLower();
                Guid fileGuid = Guid.NewGuid();
                string fileName = fileGuid + fileExtension;

                if (fileExtension == ".mp4" || fileExtension == ".mov" || fileExtension == ".avi" || fileExtension == ".wmv")
                {
                    emp.ImageUrl = fileName;
                    // Save the file and set the VideoUrl
                    var filePath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "videos", fileName);
                  
                    using (var stream = new FileStream(filePath, FileMode.Create))
                    {
                        mediaFile.CopyTo(stream);
                    }
                    emp.VideoUrl = $"/videos/{fileName}";
                }
                else
                {
                    ModelState.AddModelError(string.Empty, "Unsupported file type.");
                    return View("Create", emp); // Return the view immediately if the file type is unsupported
                }
            }

            // 1) Create Process Info
            var psi = new ProcessStartInfo();
            psi.FileName = @"C:\Python311\python.exe";
            // 2) Provide script and arguments
            var script = @"D:\GP final\Employees_System-master\MVC2\script.py";
            string hi = mediaFile?.FileName ?? string.Empty;

            psi.Arguments = $"\"{script}\" \"{hi}\"";

            // 3) Process configuration
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            // 4) Execute process and get output
            var errors = "";
            string results = "";

            using (var process = Process.Start(psi))
            {
                if (process != null)
                {
                    // Wait for the process to complete
                    process.WaitForExit();

                    // Read the output streams
                    errors = process.StandardError.ReadToEnd();
                    results = process.StandardOutput.ReadToEnd();
                }
            }

           /* if (!string.IsNullOrEmpty(errors))
            {
                ModelState.AddModelError(string.Empty, errors);
                return View("Create", emp);
            }*/

            emp.FullName = results;
            return View("Create", emp);
        }


    }
}
